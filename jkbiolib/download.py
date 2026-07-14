import os
from ftplib import FTP

def download_ftp_chunk(
    host: str, 
    remote_filepath: str, 
    local_filepath: str, 
    start_byte: int, 
    chunk_size: int,
    username: str = '',
    password: str = ''
):
    ftp = FTP(host)
    if (username == '') and (password == ''):
        ftp.login() 
    else:
        ftp.login(user=username, passwd=password)
        
    ftp.voidcmd('TYPE I')
    bytes_downloaded = 0

    with open(local_filepath, 'wb') as f:
        def callback(data):
            nonlocal bytes_downloaded
            remaining_bytes = chunk_size - bytes_downloaded
            
            if remaining_bytes <= 0:
                return
                
            if len(data) > remaining_bytes:
                data = data[:remaining_bytes]
                
            f.write(data)
            bytes_downloaded += len(data)
            
            if bytes_downloaded >= chunk_size:
                print(f"Target chunk of {chunk_size} bytes reached. Closing connection.")
                ftp.close() 

        try:
            # FIX: Use sendcmd instead of voidcmd to accept the 350 response code
            ftp.sendcmd(f'REST {start_byte}')
            
            ftp.retrbinary(f'RETR {remote_filepath}', callback)
        except Exception as e:
            # If the exception happened because we manually closed the connection, it's a success
            if bytes_downloaded >= chunk_size:
                print("Chunk successfully isolated.")
            else:
                print(f"Transfer stopped due to an error: {e}")
        finally:
            try:
                ftp.quit()
            except:
                pass
