from webcrawling.androidrank_crawler import get_applist
from webcrawling.playstore_crawler import get_policy
import pandas as pd


def get_package_names_from_applist():
    applist = pd.read_csv('backend/src/webcrawling/applist.csv')
    packages = applist.iloc[0:5, 0]
    return packages


# Run Script
if __name__ == '__main__':

    # Get the package names for the defined category
    category = "Communication"
    number = 5

    applist = get_applist(category, number)
    print(f'Top {number} of {category}: ', '\n', applist, '\n')

    # package_names = get_package_names_from_applist()

    for app_name in applist:
        print(f'Getting policy for {app_name}')
        get_policy(app_name)
        print('Success', '\n')

