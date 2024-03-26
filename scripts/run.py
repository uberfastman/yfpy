
from Hitters import build_available_hitters, build_my_hitters
from scripts.RP import build_available_rp, build_my_rp
from scripts.SP import build_available_sp, build_my_sp

from scripts.yahoo_driver import get_yahoo_driver, get_available_hitters, get_my_hitters, get_available_rp, get_my_RP, get_available_sp, get_my_SP
from scrapers.pl_scraper import get_hitterlist, get_pitcherlist, get_hold_up
from scrapers.eno_scraper import get_eno_rankings
from scrapers.ss_scraper import get_ss_rankings
from scrapers.razz_scraper import get_gray_hitters, get_gray_pitchers
from scrapers.roto_scraper import get_roto_hitters, get_roto_pitchers
from scrapers.local_files import get_local_file


driver = get_yahoo_driver()
my_hitters = get_my_hitters(driver)
my_rp = get_my_RP(driver)
my_sp = get_my_SP(driver)
available_hitters = get_available_hitters(driver)
available_rp = get_available_rp(driver)
available_sp = get_available_sp(driver)


my_ranks = get_local_file(r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\my_ranks.csv")
razz_OPS = get_local_file(r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\razz_OBP_SLG.csv")
razz_100 = get_local_file(r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\razz_100_hitters.csv")
gray_hitters = get_gray_hitters()
hitterlist = get_hitterlist('https://pitcherlist.com/top-150-hitters-for-fantasy-baseball-2024-3-22-update/')
rotoballer = get_roto_hitters('https://www.rotoballer.com/fantasy-baseball-rankings/440514#!/rankings?spreadsheet=mixed&league=Hitters')


gray_sp = get_gray_pitchers()
pitcherlist = get_pitcherlist('https://pitcherlist.com/top-100-starting-pitchers-for-2024-fantasy-baseball-3-21-update/')
rotoballer = get_roto_pitchers('https://www.rotoballer.com/fantasy-baseball-rankings/440514#!/rankings?spreadsheet=mixed&league=SP')
ss_ranks = get_ss_rankings()
eno_ranks = get_eno_rankings()


hold_up = get_hold_up('https://pitcherlist.com/the-hold-up-3-15-update-top-100-relievers-for-holds-in-2024/')

build_available_hitters(available_hitters=available_hitters,
                        my_ranks=my_ranks,
                        razz_OPS=razz_OPS,
                        razz_100=razz_100,
                        gray_hitters=gray_hitters,
                        hitterlist=hitterlist,
                        rotoballer=rotoballer,)

build_available_sp(available_sp=available_sp,
                    gray_sp=gray_sp,
                    pitcherlist=pitcherlist,
                    rotoballer=rotoballer,
                    ss_ranks=ss_ranks,
                    eno_ranks=eno_ranks,
                    )

build_available_rp(available_rp=available_rp,
                    hold_up=hold_up,
                    )

build_my_hitters(my_hitters=my_hitters,
                    my_ranks=my_ranks, 
                    razz_OPS=razz_OPS, 
                    razz_100=razz_100, 
                    gray_hitters=gray_hitters, 
                    hitterlist=hitterlist, 
                    rotoballer=rotoballer,
                    )

build_my_sp(my_sp=my_sp, 
            gray_sp=gray_sp, 
            pitcherlist=pitcherlist, 
            rotoballer=rotoballer, 
            ss_ranks=ss_ranks, 
            eno_ranks=eno_ranks,
            )

build_my_rp(my_rp=my_rp, 
            hold_up=hold_up,
            )