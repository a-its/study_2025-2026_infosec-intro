#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

int main(void)
{
    uid_t uid = geteuid();
    gid_t gid = getegid();
    printf("uid=%u, gid=%u\n",
           (unsigned int)uid, (unsigned int)gid);
    return 0;
}
