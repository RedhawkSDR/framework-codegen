def canonicalName(name):
    """
    Returns the canonical name for the target 'name'. This is the prefix that
    should be used for all related variables (e.g. "target_SOURCES").

    From the Automake manual:
      All characters in the name except for letters, numbers, the strudel (@),
      and the underscore are turned into underscores when making macro
      references.
    """
    retval = ''
    for ch in name:
        if (ch.isalnum() or ch == '@'):
            retval += ch
        else:
            retval += '_'
    return retval
