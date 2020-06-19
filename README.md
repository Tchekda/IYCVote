# IYC Vote

It was fun to vote every 3 hours, but I thought : Why wouldn't I use my skills to make my life easier

## Warning
Even if the rules don't specify, using a bot to vote is forbidden on IYC, use at your own risks !

## Setup

### Requirements
 * Python 3 
 * pip3

### Installation
 * Clone the code `git clone https://github.com/Tchekda/IYCVote.git`
 * Go in the directory `cd IYCVote/`
 * Install pip dependencies `pip install -r requirements.txt`
 * Create the voter service `ln -S vote.service /etc/systemd/system/` with your user, change each "CHANGEME"
 * Set your IYC login and password as environnement variables : `IYC_USERNAME` and `IYC_PASSWORD` in service file for example
 * Create log file at `/var/log/cron/vote.log` with write access for the user. Or change [this line](https://github.com/Tchekda/IYCVote/blob/82cc6970b3167bc5ef8c6fb27ea9a4bea5eb36dc/vote.py#L51)
 * Reload and start the script `sudo systemctl daemon-reload && sudo systemctl enable --now vote`
 * Enjoy !

## Contribution and Issues
Feel free to open issues if you have a problem or create a pull-request to make this bot better !