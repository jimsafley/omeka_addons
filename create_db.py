import argparse
import omekaaddons

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create the omekaaddons database')
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    db = omekaaddons.Db()
    db.create_db()

    if args.test:
        test_addons = [
            ('omeka', 'plugin-ExhibitBuilder', 'classic_plugin', 'ExhibitBuilder'),
            ('omeka', 'plugin-Reports', 'classic_plugin', 'Reports'),
            ('omeka', 'plugin-ZoteroImport', 'classic_plugin', 'ZoteroImport'),
            ('omeka', 'plugin-Geolocation', 'classic_plugin', 'Geolocation'),
            ('omeka', 'plugin-Scripto', 'classic_plugin', 'Scripto'),
            ('omeka', 'plugin-Contribution', 'classic_plugin', 'Contribution'),
        ]
        for test_addon in test_addons:
            db.insert_addon(*test_addon)
