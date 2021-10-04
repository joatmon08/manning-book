from google.cloud import billing_v1

HOURS_IN_MONTH = 730
NANO_UNITS = 10**-9


class ComputeSKU:
    def __init__(self, machine_type, service_name):
        self.billing = \
            billing_v1.services.cloud_catalog.CloudCatalogClient()
        self.service_name = service_name
        type_name = machine_type.split('-')
        self.family = type_name[0]
        self.exclude = [
            'custom',
            'preemptible',
            'sole tenancy',
            'commitment'
        ] if type_name[1] == 'standard' else []

    def _filter(self, description):
        return not any(
            type in description for type in self.exclude
        )

    def _get_unit_price(self, result):
        expression = result.pricing_info[0]
        unit_price = expression. \
            pricing_expression.tiered_rates[0].unit_price.nanos \
            if expression else 0
        category = result.category.resource_group
        if category == 'CPU':
            self.cpu_pricing = unit_price
        if category == 'RAM':
            self.ram_pricing = unit_price

    def get_pricing(self, region):
        for result in self.billing.list_skus(parent=self.service_name):
            description = result.description.lower()
            if region in result.service_regions and \
                    self.family in description and \
                    self._filter(description):
                self._get_unit_price(result)
        return self.cpu_pricing, self.ram_pricing


class ComputeService:
    def __init__(self):
        self.billing = \
            billing_v1.services.cloud_catalog.CloudCatalogClient()
        for result in self.billing.list_services():
            if result.display_name == 'Compute Engine':
                self.name = result.name


def calculate_monthly_compute(machine_type, region):
    service_name = ComputeService().name
    sku = ComputeSKU(machine_type.name, service_name)
    cpu_price, ram_price = sku.get_pricing(region)

    cpu_cost = machine_type.cpus * cpu_price * \
        HOURS_IN_MONTH if cpu_price else 0
    ram_cost = machine_type.ram * ram_price * \
        HOURS_IN_MONTH if ram_price else 0
    return (cpu_cost + ram_cost) * NANO_UNITS
