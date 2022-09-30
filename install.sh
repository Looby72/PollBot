rm -rf Bot
VERSION="v0.2"
URL="https://github.com/Looby72/PollBot/releases/download/${VERSION}/PollBot.zip"
FILENAME="Bot${VERSION}.zip"
curl -L $URL -o $FILENAME
unzip $FILENAME
rm $FILENAME
cd Bot