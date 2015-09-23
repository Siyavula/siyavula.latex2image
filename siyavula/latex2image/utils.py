import os
import errno
import shutil


def mkdir_p(path):
    ''' mkdir -p functionality
    from:
    http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    '''
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def copy_if_newer(src, dest):
    ''' Copy a file from src to  dest if src is newer than dest

    Returns True if success or False if there was a problem
    '''
    success = True
    dest_dir = os.path.dirname(dest)
    if (dest_dir is None) or (src is None):
        success = False
        return success
    if not os.path.exists(dest_dir):
        mkdir_p(dest_dir)

    if os.path.exists(src):
        # check whether src was modified more than a second after dest
        # and only copy if that was the case
        srcmtime = os.path.getmtime(src)
        try:
            destmtime = os.path.getmtime(dest)
            if srcmtime - destmtime > 1:
                shutil.copy2(src, dest)

        except OSError:
            # destination doesn't exist
            shutil.copy2(src, dest)
    else:
        success = False

    return success
