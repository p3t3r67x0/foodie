#!/usr/bin/env python3


import openfoodfacts


def main():
    products = openfoodfacts.products.get_all_by_country('germany')

    for product in products:
        print(product)


if __name__ == '__main__':
    main()
