#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

int main(void)
{
    uid_t real_uid = getuid();
    uid_t e_uid = geteuid();
    gid_t real_gid = getgid();
    gid_t e_gid = getegid();
    printf("e_uid=%u, e_gid=%u\n",
           (unsigned int)e_uid, (unsigned int)e_gid);
    printf("real_uid=%u, real_gid=%u\n",
           (unsigned int)real_uid, (unsigned int)real_gid);
    return 0;
}
