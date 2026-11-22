import os
import tempfile

os.environ["CRU_DATABASE_PATH"] = tempfile.mktemp(suffix=".db")
os.environ["SECRET_KEY"] = "test-secret"
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_PASSWORD"] = "test-admin-pw"

from app import app  # noqa: E402

client = app.test_client()
failures = []


def check(condition, msg):
    if not condition:
        failures.append(msg)
        print("FAIL:", msg)
    else:
        print("ok:", msg)


# --- public pages ---
r = client.get("/")
check(r.status_code == 200, f"GET / -> {r.status_code}")
check(b"Cookie Runners HQ" in r.data, "dashboard contains brand")
check(b"Featured Cookie Run Games" in r.data, "dashboard featured games section")

r = client.get("/games")
check(r.status_code == 200, f"GET /games -> {r.status_code}")
check(b"Cookie Run: Kingdom" in r.data, "games list shows Kingdom")

r = client.get("/games/cookie-run-kingdom")
check(r.status_code == 200, f"GET /games/cookie-run-kingdom -> {r.status_code}")
check(b"Official website" in r.data, "game detail has official links")

r = client.get("/games/does-not-exist")
check(r.status_code == 404, f"GET missing game -> {r.status_code} (got {r.status_code})")

r = client.get("/tracker")
check(r.status_code == 200, f"GET /tracker -> {r.status_code}")
check(b"Devsisters Update Tracker" in r.data, "tracker page")
check(b"Confirmed" in r.data, "tracker shows confirmation badges")

r = client.get("/tracker/welcome-to-cookie-runners-hq")
check(r.status_code == 200, f"GET announcement detail -> {r.status_code}")

r = client.get("/tracker/does-not-exist")
check(r.status_code == 404, f"GET missing announcement -> {r.status_code}")

r = client.get("/upcoming")
check(r.status_code == 200, f"GET /upcoming -> {r.status_code}")

r = client.get("/calendar")
check(r.status_code == 200, f"GET /calendar -> {r.status_code}")
check(b"Update Calendar" in r.data, "calendar page renders (grid or empty state)")

r = client.get("/calendar?view=week")
check(r.status_code == 200, f"GET /calendar?view=week -> {r.status_code}")

# calendar grid with an in-range item
with client.application.app_context():
    from database import add_calendar_item
    add_calendar_item({"title": "Test Calendar Launch", "description": "d", "item_type": "launch",
                       "start_date": "2026-11-25", "end_date": None, "all_day": 1, "game_id": None,
                       "url": "", "confirmation_status": "confirmed"})
r = client.get("/calendar")
check(b"cal-grid" in r.data and b"Test Calendar Launch" in r.data, "calendar grid shows in-range item")

r = client.get("/search?q=kingdom")
check(r.status_code == 200, f"GET /search?q=kingdom -> {r.status_code}")

for path in ("/api/games", "/api/announcements", "/api/events", "/api/calendar"):
    r = client.get(path)
    check(r.status_code == 200 and r.is_json, f"GET {path} -> {r.status_code} json={r.is_json}")

# --- admin auth ---
r = client.get("/admin")
check(r.status_code == 302, f"GET /admin without login -> {r.status_code} (redirect expected)")

r = client.get("/admin/login")
check(r.status_code == 200, f"GET /admin/login -> {r.status_code}")

r = client.post("/admin/login", data={"username": "admin", "password": "wrong"})
check(r.status_code == 200 and b"Invalid" in r.data, "bad credentials rejected")

r = client.post("/admin/login", data={"username": "admin", "password": "test-admin-pw"})
check(r.status_code == 302, f"POST /admin/login valid -> {r.status_code}")

with client.session_transaction() as sess:
    check(sess.get("admin_user", {}).get("username") == "admin", "admin session set")

r = client.get("/admin")
check(r.status_code == 200, f"GET /admin with login -> {r.status_code}")

# --- admin CRUD: games ---
r = client.post("/admin/games", data={
    "title": "Test Game Cookie", "slug": "test-game-cookie", "short_description": "A test game",
    "release_date": "2027-01-01", "platforms": "iOS, Android", "developer": "Devsisters",
    "publisher": "Devsisters", "status": "Officially announced", "game_type": "upcoming",
    "confirmation_status": "rumour", "featured": "on", "image_url": "",
    "official_website": "https://example.com", "announcement_link": "", "trailer_url": "",
    "description": "Test description", "notes": "Test note — rumour",
})
check(r.status_code == 302, f"POST add game -> {r.status_code}")

r = client.get("/games?q=test+game+cookie")
check(b"Test Game Cookie" in r.data, "added game searchable")

# find id
with client.application.app_context():
    from database import get_games
    tg = [g for g in get_games() if g["slug"] == "test-game-cookie"][0]
    gid = tg["id"]

r = client.get(f"/admin/games/{gid}/edit")
check(r.status_code == 200, f"GET edit game {gid} -> {r.status_code}")

r = client.post(f"/admin/games/{gid}/edit", data={
    "title": "Test Game Cookie Updated", "slug": "test-game-cookie", "short_description": "Updated",
    "release_date": "2027-02-02", "platforms": "iOS", "developer": "Devsisters",
    "publisher": "Devsisters", "status": "Released", "game_type": "other",
    "confirmation_status": "confirmed", "featured": "", "image_url": "",
    "official_website": "", "announcement_link": "", "trailer_url": "",
    "description": "Updated desc", "notes": "",
})
check(r.status_code == 302, f"POST edit game -> {r.status_code}")

r = client.post(f"/admin/games/{gid}/delete", data={})
check(r.status_code == 302, f"POST delete game -> {r.status_code}")
with client.application.app_context():
    from database import get_game
    check(get_game("test-game-cookie") is None, "deleted game gone")

# --- admin CRUD: announcements ---
r = client.post("/admin/announcements", data={
    "title": "Test Announcement", "slug": "test-announcement", "summary": "A summary",
    "category_id": "1", "announcement_type": "news", "confirmation_status": "speculation",
    "published_at": "2026-11-22", "source_url": "", "source_name": "",
    "is_pinned": "", "is_published": "on", "content": "Full test content.",
})
check(r.status_code == 302, f"POST add announcement -> {r.status_code}")

with client.application.app_context():
    from database import get_announcement
    ta = get_announcement("test-announcement")
    check(ta is not None, "announcement added")
    aid = ta["id"]

r = client.get(f"/admin/announcements/{aid}/edit")
check(r.status_code == 200, f"GET edit announcement {aid} -> {r.status_code}")

r = client.post(f"/admin/announcements/{aid}/delete", data={})
check(r.status_code == 302, f"POST delete announcement -> {r.status_code}")
with client.application.app_context():
    from database import get_announcement
    check(get_announcement("test-announcement") is None, "deleted announcement gone")

# --- admin CRUD: updates ---
with client.application.app_context():
    from database import get_games, add_update
    gid = get_games()[0]["id"]
    add_update({"game_id": gid, "title": "Test Update", "version": "v1", "patch_notes": "notes",
                "release_date": "2026-11-01", "maintenance": 0, "source_url": "",
                "confirmation_status": "confirmed"})

r = client.post("/admin/updates", data={
    "game_id": str(gid), "title": "Test Update 2", "version": "v2", "patch_notes": "more notes",
    "release_date": "2026-12-01", "maintenance": "on", "source_url": "",
    "confirmation_status": "rumour",
})
check(r.status_code == 302, f"POST add update -> {r.status_code}")

with client.application.app_context():
    from database import get_updates
    ups = get_updates()
    tu = [u for u in ups if u["title"] == "Test Update 2"][0]
    uid = tu["id"]
r = client.post(f"/admin/updates/{uid}/delete", data={})
check(r.status_code == 302, f"POST delete update -> {r.status_code}")

# --- admin CRUD: events ---
with client.application.app_context():
    from database import get_games, add_event, get_events
    gid = get_games()[0]["id"]
    add_event({"game_id": gid, "title": "Test Event", "description": "desc", "start_date": "2026-12-01",
               "end_date": "2026-12-02", "event_type": "event", "image_url": "", "source_url": "",
               "confirmation_status": "confirmed"})
    evs = [e for e in get_events() if e["title"] == "Test Event"]
    eid = evs[0]["id"]

r = client.post(f"/admin/events/{eid}/delete", data={})
check(r.status_code == 302, f"POST delete event -> {r.status_code}")

# --- admin CRUD: calendar ---
with client.application.app_context():
    from database import get_calendar_items, add_calendar_item
    add_calendar_item({"title": "Test Calendar Item", "description": "d", "item_type": "launch",
                       "start_date": "2026-11-22", "end_date": None, "all_day": 1, "game_id": None,
                       "url": "", "confirmation_status": "confirmed"})
    citems = [c for c in get_calendar_items() if c["title"] == "Test Calendar Item"]
    cid = citems[0]["id"]
r = client.post(f"/admin/calendar/{cid}/delete", data={})
check(r.status_code == 302, f"POST delete calendar item -> {r.status_code}")

# --- admin CRUD: categories ---
r = client.post("/admin/categories", data={"name": "Test Category", "slug": "test-category",
                                           "description": "d", "color": "#ff0000"})
check(r.status_code == 302, f"POST add category -> {r.status_code}")
with client.application.app_context():
    from database import get_category
    tc = get_category("test-category")
    check(tc is not None, "category added")
    cid = tc["id"]
r = client.post(f"/admin/categories/{cid}/delete", data={})
check(r.status_code == 302, f"POST delete category -> {r.status_code}")

# --- logout ---
r = client.get("/admin/logout")
check(r.status_code == 302, f"GET /admin/logout -> {r.status_code}")

# --- seed checks ---
with client.application.app_context():
    from database import get_games, get_announcements, get_events
    titles = [g["title"] for g in get_games()]
    check("Cookie Run: Kingdom" in titles, "seeded: Kingdom")
    check("Cookie Run: OvenBreak" in titles, "seeded: OvenBreak")
    check("Cookie Run: Tower of Adventures" in titles, "seeded: Tower of Adventures")
    check(any("Witch" in t for t in titles), "seeded: Witch's Castle (rumour)")
    anns = get_announcements()
    check(any("Rumour" in (a["title"] or "") or a["confirmation_status"] == "rumour" for a in anns),
          "seeded rumour announcement present")
    evs = get_events()
    check(len(evs) >= 1, "seeded events present")

print()
if failures:
    print(f"{len(failures)} FAILURES")
    raise SystemExit(1)
print("ALL SMOKE TESTS PASSED")
