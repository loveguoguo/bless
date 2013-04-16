#!/bin/sh
#
# Usage: `basename $0` [OPTION]... [VAR=VALUE]...
#

set -e

src_dir=`dirname $0`

PREFIX=/home/project/bless/bless

# For convenient, run-user will be set as current user.
# For safety, project owner should not be set as root automoticly. If current
# user is root, run-user will be set as nobody.
USER=`whoami`
if [ $USER = 'root' ]; then
	USER="nobody"
fi
GROUP=`id -gn $USER`

#
EXCLUDE_FROM="$src_dir/exclude.txt"


# util functions
usage() {
cat << _EOF

Usage: ./install.sh [OPTION]... [VAR=VALUE]...

Installation directories:
  --prefix=[dir]         project installation directory, default is
                         [$PREFIX]

For better control, use the options below.
  --user=[user]          the system user who run this program, default is
                         [$USER]
  --group=[group]        the system group who run this program, default is
                         [$GROUP]
  --exclude-from=[file]  read exclude patterns from file, default is
                         [$EXCLUDE_FROM]
  --run-user=[user]      same as --user, deprecated
  --run-group=[group]    same as --group, deprecated
  --help                 print this help messages.

_EOF
}

for arg do
	case "$arg" in
	--prefix=*) PREFIX=`echo "$arg" | sed -e "s;--prefix=;;"` ;;
	--user=*) USER=`echo "$arg" | sed -e "s;--user=;;"` ;;
	--group=*) GROUP=`echo "$arg" | sed -e "s;--group=;;"` ;;
	--exclude-from=*) EXCLUDE_FROM=`echo "$arg" | sed -e "s;--exclude-from=;;"` ;;
	--run-user=*) USER=`echo "$arg" | sed -e "s;--run-user=;;"` ;;
	--run-group=*) GROUP=`echo "$arg" | sed -e "s;--run-group=;;"` ;;
	*)
		usage 
		exit 1
		;;
	esac
done


#
exec_files="$PREFIX/wsgi_handler.py"

echo "The following files will be installed..."
exclude_str=$(
cat $EXCLUDE_FROM | while read line;
do
	if test -z "$line"; then
		continue
	fi
	leading_char=`echo "$line" | cut -c1`
	if test "$leading_char" = "#"; then
		continue
	fi

	echo -n " -name \"$line\" -prune -o"
done)

cd $src_dir
find_cmd="find . $exclude_str -print0 | cpio -pamdvu0 --quiet $PREFIX"
eval $find_cmd
echo

echo "Change owner (-R $USER:$GROUP)..."
chown -R $USER:$GROUP $PREFIX
echo

#echo "Set \`etc' directory 700 permission..."
#chmod 700 $PREFIX/etc
#echo

echo "Set $exec_files executable..."
chmod +x $exec_files
echo

echo "Update file timestamp..."
touch $exec_files
echo

echo "Done (maybe you should edit config files manually!)"

############################
# You may write your specifical scripts here...

