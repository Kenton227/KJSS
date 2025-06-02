from mock_data import (
    gen_users,
    gen_games,
    gen_showcases,
    gen_views,
    gen_comments,
    gen_reports
)

if __name__ == "__main__":
    print("Loading demo data...")
    gen_users(80)
    gen_games(500)
    gen_showcases(750)
    gen_views(3000)
    gen_comments(1000)
    gen_reports(30)
    print("Finished loading demo data!")