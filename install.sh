rm -rf Bot
VERSION="v0.2" #exmaple version, change it to the version you want to download from the github release page
URL="https://github.com/Looby72/PollBot/releases/download/${VERSION}/PollBot.zip"
FILENAME="Bot${VERSION}.zip"
curl -L $URL -o $FILENAME
unzip $FILENAME
rm $FILENAME
cd Bot