# Git Upload Steps

Create an empty GitHub repository named:

```text
CAD-Controller-Anomaly-Detection
```

Then run these commands inside the local folder:

```powershell
cd "C:\Users\ryhan\My Drive\Github\CAD-Controller-Anomaly-Detection"

git init
git add .
git commit -m "Initial commit for CAD framework"

git branch -M main
git remote add origin https://github.com/ryhanuddin/CAD-Controller-Anomaly-Detection.git
git push -u origin main
```
