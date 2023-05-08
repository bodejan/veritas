from androidrank_crawler import get_applist
from playstore_crawler import get_policy
import pandas as pd


def get_package_names_from_applist():
    applist = pd.read_csv('applist.csv')
    packages = applist.iloc[0:5, 0]
    return packages


# Run Script
if __name__ == '__main__':

    # Get the package names for the defined category
    category = "COMMUNICATION"
    num = 10
    # get_package_names(category, num) Todo: Implement this function in the androidrank crawler

    # Get the csv of the 500 most popular apps
    # get_applist()

    package_names = get_package_names_from_applist()

    for package_name in package_names:
        print(package_name)
        get_policy(package_name)

    # Test if it is possible to crawl a specific policy
    # policy_id = "com.ustwo.monumentvalley"   # 'org.coursera.android'
    # get_policy(policy_id)

