"""
Werkzeug launcher for application

Source: Professor Eddy's werk.py file
"""

import traceback

from bank import app

if __name__ == '__main__':

    # pylint: disable=W0703
    try:
        app.run(debug=app.debug, host='localhost', port=8097)
    except Exception as err:
        traceback.print_exc()
