apt-get update
apt-get upgrade -y

# apt-get install software-properties-common
# add-apt-repository ppa:webupd8team/java
# apt-get update
# apt-get install oracle-java8-installer

mkdir -p /opt/hadoop-3.1.1
cd /opt/hadoop-3.1.1/
wget http://xenia.sote.hu/ftp/mirrors/www.apache.org/hadoop/common/hadoop-3.1.1/hadoop-3.1.1.tar.gz
tar xzf hadoop-3.1.1.tar.gz
export HADOOP_HOME=/opt/hadoop-3.1.1
export HADOOP_USER_CLASSPATH_FIRST=true
export JAVA_HOME=/usr/lib/jvm/java-8-oracle/jre

cd /opt
wget http://xenia.sote.hu/ftp/mirrors/www.apache.org/hive/hive-3.1.0/apache-hive-3.1.1-bin.tar.gz
tar xzf apache-hive-3.1.1-bin.tar.gz