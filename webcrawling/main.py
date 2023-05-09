from androidrank_crawler import get_applist
from playstore_crawler import get_policy
import pandas as pd


def get_package_names_from_applist():
    applist = pd.read_csv('webcrawling/applist.csv')
    packages = applist.iloc[0:5, 0]
    return packages


# Run Script
if __name__ == '__main__':

    # Get the package names for the defined category
    category = "Communication"
    number = 5

    applist = get_applist(category, number)

    # package_names = get_package_names_from_applist()

    for app_name in applist:
        print(app_name)
        get_policy(app_name)

