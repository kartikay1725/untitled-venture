# Rollback Procedure

If a deployment fails or a critical issue is detected post‑deployment, rollback to the previous stable release.

## Steps

1. Identify the deployment ID to rollback:
   ```bash
   railway deployments | grep "failed" | awk '{print $1}'
   ```
2. Execute rollback:
   ```bash
   railway run deploy rollback --deployment-id <DEPLOYMENT_ID>
   ```
3. Verify the rollback:
   ```bash
   curl -I https://<app>.railway.app/health
   ```
4. Notify the team via Slack channel `#ops`.

## Notes
- All rollback commands are idempotent.
- Ensure the environment variables are unchanged.
- Monitor logs for any residual errors after rollback.