---
description: Entire.io Setup Guide
---

# Entire.io Integration

Entire.io is the observability layer for Swagentics, designed to capture conversations, prompts, and architectural decisions seamlessly alongside your git commits. 

## Windows Installation Guide (Using Scoop)

We rely on `scoop` to install the `entire` CLI on Windows.

1. **Add the Repository Bucket:**
   ```powershell
   scoop bucket add entire https://github.com/entireio/scoop-bucket.git
   ```

2. **Install the CLI:**
   ```powershell
   scoop install entire/cli
   ```

3. **Authenticate:**
   ```powershell
   entire login
   ```
   *(This will open a browser window to link your local CLI to your Entire.io account).*

4. **Enable in your Repository:**
   Navigate to your project folder (e.g., `vorteg/swagentics`) and run:
   ```powershell
   entire enable
   ```

## Daily Usage
Once `entire enable` is run in your repository, Entire.io automatically instruments your local Git hooks. Every time you or Antigravity make a commit, the session context will be checkpointed to the hidden branch `entire/checkpoints/v1` and pushed to your dashboard. No manual logging required!
