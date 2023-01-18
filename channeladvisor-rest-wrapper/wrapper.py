from .ca_token import ChannelAdvisorToken
import requests
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
import logging

# print(get_token())

class ChannelAdvisor:
    def __init__(self, client_id, client_secret, refresh_token, api_endpoint = 'https://api.channeladvisor.com', logger: logging.Logger = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.api_endpoint = api_endpoint

        self.token_interface = ChannelAdvisorToken(client_id, client_secret, refresh_token)
        self._logger = logger or logging.getLogger(__name__)


    def get_products(self, options, only_products = True):
        "Returns the products matching this request. If the product result set is multiple pages, only the first is returned."

        params = self.get_params(options)

        # print(params)

        resource = "/v1/Products"

        if ("productId" in options):
            resource += "(" + options["productId"] + ")"

        request_options = {
            "method": 'GET',
            "resource": resource,
            "params": params,
            "body": None,
        }

        # print(request_options)

        data = self.__make_request(request_options)

        if (only_products):
            return data["value"]
        else:
            return data

    def get_all_products(self, options):
        """Returns all the products from ChannelAdvisor that match a given set of parameters."""

        products = []

        more_products = True

        while more_products:
            # print(options)

            data = self.get_products(options, only_products=False)


            products = products + data["value"]

            if "@odata.nextLink" in data:
                # print(data["@odata.nextLink"])
                parsed_url = urlparse(data["@odata.nextLink"])
                captured_value = parse_qs(parsed_url.query)['$skip'][0]

                options["skip"] = captured_value
            else:
                more_products = False
    
        return products

    def get_product_by_sku(self):
        """Returns a product object from ChannelAdvisor given a SKU."""
        print("no")

    def get_product_attributes(self, options):
        print("no")

    def update_product(self, options):
        """Updates a product with the supplied values."""
        print("no")

    def update_product_attributes(self, options):
        if not "product_id" in options:
            raise Exception("'product_id' is required.")
        
        params = self.get_params(options)

        resource = "/v1/Products" + "(" + str(options["product_id"]) + ")" + "/UpdateAttributes"

        request_options = {
            'method': 'POST',
            'resource': resource,
            'params': params,
            'body': options['body'],
        }
        # print(request_options)

        data = self.__make_request(request_options)


    def update_product_image(self, options):
        if not "product_id" in options:
            raise Exception("'product_id' is required.")

        if not "placement_name" in options:
            raise Exception("'placement_name' is required.")
          
        params = self.get_params(options)

        resource = "/v1/Products" + "(" + str(options["product_id"]) + ")/Images('" + options["placement_name"] + "')"

        request_options = {
            'method': 'PUT',
            'resource': resource,
            'params': params,
            'body': options['body'],
        }

        data = self.__make_request(request_options)


    def __make_request(self, options):
        """Sends a request."""
        token = self.token_interface.get_token()

        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }

        http_method = options["method"]
        full_url = self.api_endpoint + options["resource"]
        ep_params = options["params"]
        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"

        # print(options)

        response = requests.request(
            http_method,
            params=options["params"],
            headers=headers,
            url=full_url,
            json=options["body"]
        )

        # print(response.request.body)

        try:
            self._logger.debug(msg=log_line_pre)
            data_out = response.json()

            if response.status_code >= 200 and response.status_code <= 299:     # OK
                raise Exception({response.status_code, data_out["Message"]})
            
            return data_out
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))



    def get_params(self, options):
        params = {}

        if ("filter" in options):
            params['$filter'] = " and ".join(options["filter"]) 
        if ("select" in options):
            params['$select'] = " and ".join(options["select"])
        if ("expand" in options):
            params['$expand'] = ",".join(options["expand"])
        if ("skip" in options):
            params['$skip'] = options["skip"]
        if ("top" in options):
            params['$top'] = options["top"]

        return params
