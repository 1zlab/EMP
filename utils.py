def rainbow(output, color=None):
    """
    字符串彩色输出
    """
    if color:
        if color == 'green':
            return '\033[1;32m%s\033[0m' % output
        if color == 'red':
            return '\033[1;31m%s\033[0m' % output
        if color == 'blue':
            return '\033[1;34m%s\033[0m' % output
    else:
        return output
