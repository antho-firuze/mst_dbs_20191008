import logging
import boto3
from botocore.exceptions import ClientError

def create_vault(vault_name):
    """Create an Amazon Glacier vault.

    :param vault_name: string
    :return: glacier.Vault object if vault was created, otherwise None
    """

    glacier = boto3.resource('glacier')
    try:
        vault = glacier.create_vault(vaultName=vault_name)
    except ClientError as e:
        logging.error(e)
        return None
    return vault

def list_vaults(max_vaults=10, iter_marker=None):
    """List Amazon S3 Glacier vaults owned by the AWS account

    :param max_vaults: Maximum number of vaults to retrieve
    :param iter_marker: Marker used to identify start of next batch of vaults
    to retrieve
    :return: List of dictionaries containing vault information
    :return: String marking the start of next batch of vaults to retrieve.
    Pass this string as the iter_marker argument in the next invocation of
    list_vaults().
    """

    # Retrieve vaults
    glacier = boto3.client('glacier')
    if iter_marker is None:
        vaults = glacier.list_vaults(limit=str(max_vaults))
    else:
        vaults = glacier.list_vaults(limit=str(max_vaults), marker=iter_marker)
    marker = vaults.get('Marker')       # None if no more vaults to retrieve
    return vaults['VaultList'], marker

def upload_archive(vault_name, src_data):
    """Add an archive to an Amazon S3 Glacier vault.

    The upload occurs synchronously.

    :param vault_name: string
    :param src_data: bytes of data or string reference to file spec
    :return: If src_data was added to vault, return dict of archive
    information, otherwise None
    """

    # The src_data argument must be of type bytes or string
    # Construct body= parameter
    if isinstance(src_data, bytes):
        object_data = src_data
    elif isinstance(src_data, str):
        try:
            object_data = open(src_data, 'rb')
            # possible FileNotFoundError/IOError exception
        except Exception as e:
            logging.error(e)
            return None
    else:
        logging.error('Type of ' + str(type(src_data)) +
                      ' for the argument \'src_data\' is not supported.')
        return None

    glacier = boto3.client('glacier')
    try:
        archive = glacier.upload_archive(vaultName=vault_name, body=object_data)
    except ClientError as e:
        logging.error(e)
        return None
    finally:
        if isinstance(src_data, str):
            object_data.close()

    # Return dictionary of archive information
    return archive


def main():
    """Exercise upload_archive()"""

    # Assign these values before running the program
    test_vault_name = 'INV_200212'
    filename = './destination/INV_200212/INV_AR100004174_20021202.pdf'
    # Alternatively, specify object contents using bytes.
    # filename = b'This is the data to store in the Glacier archive.'

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Upload the archive
    archive = upload_archive(test_vault_name, filename)
    if archive is not None:
        logging.info(f'Archive {archive["archiveId"]} added to {test_vault_name}')


    # """ Exercise create_vault()"""

    # # Assign this value before running the program
    # test_vault_name = 'INV_200212'

    # # Set up logging
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(levelname)s: %(asctime)s: %(message)s')

    # # Create the Glacier vault
    # vault = create_vault(test_vault_name)
    # if vault is not None:
    #     logging.info(f'Created vault {vault.name}')


    # """Exercise list_vaults()"""

    # # Set up logging
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(levelname)s: %(asctime)s: %(message)s')

    # # List the vaults
    # vaults, marker = list_vaults()
    # while True:
    #     # Print info about retrieved vaults
    #     for vault in vaults:
    #         logging.info(f'{vault["NumberOfArchives"]:3d}  'f'{vault["SizeInBytes"]:12d}  {vault["VaultName"]}')

    #     # If no more vaults exist, exit loop, otherwise retrieve the next batch
    #     if marker is None:
    #         break
    #     vaults, marker = list_vaults(iter_marker=marker)



if __name__ == '__main__':
    main()