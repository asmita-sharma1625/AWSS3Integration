CWD="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
export PYTHONPATH="$CWD"
echo $PYTHONPATH
find |grep "pyc$"|xargs rm -f
 #cd test
 python -m unittest discover -s .

