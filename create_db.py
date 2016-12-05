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
            ('omeka', 'plugin-CsvImport', 'classic_plugin', 'CsvImport'),
            ('omeka', 'plugin-Dropbox', 'classic_plugin', 'Dropbox'),
            ('omeka', 'plugin-ItemRelations', 'classic_plugin', 'ItemRelations'),
            ('omeka', 'plugin-SimpleVocab', 'classic_plugin', 'SimpleVocab'),
            ('omeka', 'plugin-SimplePages', 'classic_plugin', 'SimplePages'),
            ('omeka', 'plugin-DublinCoreExtended', 'classic_plugin', 'DublinCoreExtended'),
            ('omeka', 'plugin-OaipmhHarvester', 'classic_plugin', 'OaipmhHarvester'),
            ('omeka', 'plugin-Coins', 'classic_plugin', 'Coins'),
            ('omeka', 'plugin-GuestUser', 'classic_plugin', 'GuestUser'),
            ('omeka', 'plugin-Commenting', 'classic_plugin', 'Commenting'),
            ('omeka', 'plugin-DocsViewer', 'classic_plugin', 'DocsViewer'),
            ('omeka', 'plugin-CollectionTree', 'classic_plugin', 'CollectionTree'),
            ('omeka', 'plugin-SocialBookmarking', 'classic_plugin', 'SocialBookmarking'),
            ('omeka', 'plugin-SimpleContactForm', 'classic_plugin', 'SimpleContactForm'),
        ]
        for test_addon in test_addons:
            db.insert_addon(*test_addon)
