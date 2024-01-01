#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <jni.h>
#include <android/log.h>

#include <sys/mman.h>
#include <stdlib.h>

#include "obfuscate.h"

#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, "www", __VA_ARGS__)

void *pwn_me;

void writeAddr(uintptr_t addr, uintptr_t value) {
    size_t len = sizeof(uintptr_t);

    uintptr_t page = (uintptr_t) sysconf(_SC_PAGESIZE);
    void *start = (void *) ((uintptr_t) addr - ((uintptr_t) addr % page));
    size_t size = len + ((uintptr_t) addr % page);
    if (size % (size_t) page) {
        size += page - (size % page);
    }

    mprotect(start, size, PROT_READ | PROT_WRITE | PROT_EXEC);
    *(uintptr_t *) addr = value;
    mprotect(start, size, PROT_READ | PROT_EXEC);
}

extern "C"
JNIEXPORT void JNICALL
Java_com_aimardcr_www_MainActivity_writeAddress(JNIEnv *env, jobject thiz, jstring address,
                                                jstring value) {
    const char *addr = env->GetStringUTFChars(address, 0);
    const char *val = env->GetStringUTFChars(value, 0);

    uintptr_t addr_ptr = (uintptr_t) strtoull(addr, NULL, 16);
    uintptr_t val_ptr = (uintptr_t) strtoull(val, NULL, 16);

    writeAddr(addr_ptr, val_ptr);
}

extern "C"
JNIEXPORT jstring JNICALL
Java_com_aimardcr_www_MainActivity_getFlag(JNIEnv *env, jobject thiz) {
    const char *flag = AY_OBFUSCATE("gatauk");
    return ((jstring (*) (JNIEnv *, const char*))(pwn_me))(env, flag);
}

JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm, void* reserved) {
    JNIEnv *env;
    if (vm->GetEnv((void **) &env, JNI_VERSION_1_6) != JNI_OK) {
        return JNI_ERR;
    }

    LOGI("pwn_me: %p", &pwn_me);
    LOGI("JNIEnv->functions->ReleaseStringChars: %p", env->functions->ReleaseStringChars);

    return JNI_VERSION_1_6;
}