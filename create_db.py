import argparse
import addonregistry

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create the addonregistry database')
    parser.add_argument('--seed', action='store_true')
    args = parser.parse_args()

    db = addonregistry.Db()
    db.create_db()

    if args.seed:
        test_addons = [
            # Omeka classic plugins
            ('omeka', 'plugin-Coins', 'classic_plugin', 'Coins'),
            ('omeka', 'plugin-ExhibitBuilder', 'classic_plugin', 'ExhibitBuilder'),
            ('omeka', 'plugin-SimplePages', 'classic_plugin', 'SimplePages'),
            ('omeka', 'plugin-CollectionTree', 'classic_plugin', 'CollectionTree'),
            ('omeka', 'plugin-Commenting', 'classic_plugin', 'Commenting'),
            ('omeka', 'plugin-Contribution', 'classic_plugin', 'Contribution'),
            ('omeka', 'plugin-CSSEditor', 'classic_plugin', 'CSSEditor'),
            ('omeka', 'plugin-CsvImport', 'classic_plugin', 'CsvImport'),
            ('omeka', 'plugin-DerivativeImages', 'classic_plugin', 'DerivativeImages'),
            ('omeka', 'plugin-DocsViewer', 'classic_plugin', 'DocsViewer'),
            ('omeka', 'plugin-Dropbox', 'classic_plugin', 'Dropbox'),
            ('omeka', 'plugin-DublinCoreExtended', 'classic_plugin', 'DublinCoreExtended'),
            ('omeka', 'plugin-EmbedCodes', 'classic_plugin', 'EmbedCodes'),
            ('omeka', 'plugin-Geolocation', 'classic_plugin', 'Geolocation'),
            ('omeka', 'plugin-GuestUser', 'classic_plugin', 'GuestUser'),
            ('omeka', 'plugin-ItemOrder', 'classic_plugin', 'ItemOrder'),
            ('omeka', 'plugin-ItemRelations', 'classic_plugin', 'ItemRelations'),
            ('omeka', 'plugin-LcSuggest', 'classic_plugin', 'LcSuggest'),
            ('omeka', 'plugin-Ngram', 'classic_plugin', 'Ngram'),
            ('omeka', 'plugin-OaipmhHarvester', 'classic_plugin', 'OaipmhHarvester'),
            ('omeka', 'plugin-OmekaApiImport', 'classic_plugin', 'OmekaApiImport'),
            ('omeka', 'plugin-PdfText', 'classic_plugin', 'PdfText'),
            ('omeka', 'plugin-Posters', 'classic_plugin', 'Posters'),
            ('omeka', 'plugin-RecordRelations', 'classic_plugin', 'RecordRelations'),
            ('omeka', 'plugin-RedactElements', 'classic_plugin', 'RedactElements'),
            ('omeka', 'plugin-Reports', 'classic_plugin', 'Reports'),
            ('omeka', 'plugin-Scripto', 'classic_plugin', 'Scripto'),
            ('omeka', 'plugin-SearchByMetadata', 'classic_plugin', 'SearchByMetadata'),
            ('omeka', 'plugin-ShortcodeCarousel', 'classic_plugin', 'ShortcodeCarousel'),
            ('omeka', 'plugin-SimpleContactForm', 'classic_plugin', 'SimpleContactForm'),
            ('omeka', 'plugin-SimpleVocab', 'classic_plugin', 'SimpleVocab'),
            ('omeka', 'plugin-SocialBookmarking', 'classic_plugin', 'SocialBookmarking'),
            ('omeka', 'plugin-TextAnalysis', 'classic_plugin', 'TextAnalysis'),
            ('omeka', 'plugin-TextAnnotation', 'classic_plugin', 'TextAnnotation'),
            ('omeka', 'plugin-UserProfiles', 'classic_plugin', 'UserProfiles'),
            ('omeka', 'plugin-VraCore', 'classic_plugin', 'VraCore'),
            ('omeka', 'plugin-ZoomIt', 'classic_plugin', 'ZoomIt'),
            ('omeka', 'plugin-ZoteroImport', 'classic_plugin', 'ZoteroImport'),
            ('omeka', 'plugin-Editorial', 'classic_plugin', 'Editorial'),
            # Omeka classic themes
            ('omeka', 'theme-thanksroy', 'classic_theme', 'thanksroy'),
            ('omeka', 'theme-seasons', 'classic_theme', 'seasons'),
            ('omeka', 'theme-berlin', 'classic_theme', 'berlin'),
            ('omeka', 'theme-emiglio', 'classic_theme', 'emiglio'),
            ('omeka', 'theme-rhythm', 'classic_theme', 'rhythm'),
            ('omeka', 'theme-santa-fe', 'classic_theme', 'santa-fe'),
            ('omeka', 'theme-minimalist', 'classic_theme', 'minimalist'),
            ('omeka', 'theme-centerrow', 'classic_theme', 'centerrow'),
            ('omeka', 'theme-thedaily', 'classic_theme', 'thedaily'),
            ('omeka', 'theme-checklist', 'classic_theme', 'checklist'),
            # Omeka S modules
            ('omeka-s-modules', 'ZoteroImport', 's_module', 'ZoteroImport'),
            ('omeka-s-modules', 'ValueSuggest', 's_module', 'ValueSuggest'),
            ('omeka-s-modules', 'UnApi', 's_module', 'UnApi'),
            ('omeka-s-modules', 'Sharing', 's_module', 'Sharing'),
            ('omeka-s-modules', 'Omeka2Importer', 's_module', 'Omeka2Importer'),
            ('omeka-s-modules', 'MetadataBrowse', 's_module', 'MetadataBrowse'),
            ('omeka-s-modules', 'Mapping', 's_module', 'Mapping'),
            ('omeka-s-modules', 'FileSideload', 's_module', 'FileSideload'),
            ('omeka-s-modules', 'FedoraConnector', 's_module', 'FedoraConnector'),
            ('omeka-s-modules', 'DspaceConnector', 's_module', 'DspaceConnector'),
            ('omeka-s-modules', 'CustomVocab', 's_module', 'CustomVocab'),
            ('omeka-s-modules', 'CSVImport', 's_module', 'CSVImport'),
            ('omeka-s-modules', 'Collecting', 's_module', 'Collecting'),
            # Omeka S themes
            ('omeka-s-themes', 'thedaily', 's_theme', 'thedaily'),
            ('omeka-s-themes', 'default', 's_theme', 'default'),
            ('omeka-s-themes', 'cozy', 's_theme', 'cozy'),
            ('omeka-s-themes', 'centerrow', 's_theme', 'centerrow'),
        ]
        db.insert_addons(test_addons)
