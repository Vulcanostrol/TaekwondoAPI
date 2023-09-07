# Disclaimer!
This is **not** yet a finished API. It does not yet create pools correctly, and the configurations and settings are not
for production! If you choose to use this API to host a tournament, make sure your tournament rules are applied to the
creation of pools and you know how Django configuration works.

---

# Taekwondo API
A backend API for hosting taekwondo tournaments.

# Cloning this repository
```shell
git clone https://github.com/Vulcanostrol/TaekwondoAPI.git
```

# Initializing database
```shell
python manage.py migrate
```

# Running backend
```shell
python manage.py runserver
```

# Running tests (not optional 😉)
```shell
python manage.py test
```

# Future plans
In no specific order:
- Finish initial pool creation algorithm.
- Change settings/configuration to easily enable production mode.
- Improve documentation for frontend programmers.
- Set up CI/CD pipeline.
- Allow changing of configurations of tournament ruleset (via API).
- (maybe) add WebSocket support for live score updates.
