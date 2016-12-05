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
        ]
        for test_addon in test_addons:
            db.insert_addon(*test_addon)
