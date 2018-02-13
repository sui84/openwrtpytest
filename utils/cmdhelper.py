#coding=utf-8
import os

def ExecCmd(cmdstr):
    print cmdstr
    p=os.popen(cmdstr)
    result = p.read()
    print result
    return result

def SSHExecCmd(host,user,pwd,cmds):
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,22,user,pwd)
    for cmd in cmds:
        print cmd
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.readlines()
        print result
    ssh.close()
    return  result

def GetFile(host,usr,pwd,smbdir,srcf,dstf):
    from smb.SMBConnection import SMBConnection
    conn = SMBConnection(usr, pwd, "", "", use_ntlm_v2=True)
    conn.connect(host,445)
    #shareslist = conn.listShares()
    with open(dstf,'wb') as fobj:
        print 'get file %s%s to %s' % (smbdir,srcf,dstf)
        conn.retrieveFile(smbdir,srcf,fobj)


def GetFile2():
    # vsftpd not work
    transport = paramiko.Transport(('192.168.1.1', 22))
    transport.connect(username='root', password='pwdd')
    sftp = paramiko.SFTPClient.from_transport(transport)
    #aramiko.ssh_exception.SSHException: EOF during negotiation


