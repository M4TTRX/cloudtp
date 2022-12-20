# Cloud Technologies and Distributed Computing Labs

## Virtual env install

1. Ensure you have virtualenv on your machine

```bash
pip install virtualenv
```

2. Create the virtualenv

**macOS:**

```bash
virtualenv cloudtp-env
```

**Windows:**

```bash
python -m virtualenv cloudtp-env
```

3. Activate the virtualenv

**macOS:**

```bash
source cloudtp-env/bin/activate
```

**Windows:**
```bash
cloudtp-env/Scripts/activate
```

4. Install the requirements
```bash
pip install -r requirements.txt
```

5. Make sure you select the right kernel when running jupyter notebook by selecting the `venv` as the kernel
