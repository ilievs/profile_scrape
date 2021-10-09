if __name__ == '__main__':
    import argparse

    import web.controller.profile_controller as pweb
    import scrape.profile_scrape as pscrape

    parser = argparse.ArgumentParser(description='Profile_scrape command line tool')
    subparsers = parser.add_subparsers(title='commands',
                                       help='[command] help')

    scrape_parser = subparsers.add_parser('scrape',
                                          help='Start scraping the profiles and store them in the database')
    scrape_parser.set_defaults(command=pscrape.start_scraping)

    serve_parser = subparsers.add_parser('serve',
                                         help='Start the server for browsing the scraped results')
    serve_parser.set_defaults(command=pweb.start_server)

    args = parser.parse_args()
    args.command()
