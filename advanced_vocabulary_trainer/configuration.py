import os

# Used to access database with 'configuration.database'
package_dir = os.path.abspath(os.path.dirname(__file__))
database = os.path.join(package_dir, 'vocabulary.db')
