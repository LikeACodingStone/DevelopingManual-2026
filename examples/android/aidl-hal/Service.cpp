// Stable-AIDL HAL service using the NDK Binder API.
// Status: structure sketch, NOT built here (needs an AOSP source tree).
#include <aidl/hardware/handbook/echo/BnEcho.h>
#include <android-base/logging.h>
#include <android/binder_manager.h>
#include <android/binder_process.h>

#include <cstdlib>
#include <memory>
#include <string>

using aidl::hardware::handbook::echo::BnEcho;

class Echo : public BnEcho {
  public:
    ndk::ScopedAStatus echo(const std::string& in_text, std::string* _aidl_return) override {
        *_aidl_return = in_text;
        return ndk::ScopedAStatus::ok();
    }
};

int main() {
    // Zero extra threads: the thread that calls joinThreadPool() serves requests.
    ABinderProcess_setThreadPoolMaxThreadCount(0);

    std::shared_ptr<Echo> service = ndk::SharedRefBase::make<Echo>();
    const std::string instance = std::string(Echo::descriptor) + "/default";
    // Fails if the instance is not declared in a VINTF manifest (see hardware.handbook.echo.xml).
    binder_status_t status = AServiceManager_addService(service->asBinder().get(), instance.c_str());
    if (status != STATUS_OK) {
        LOG(ERROR) << "failed to register " << instance;
        return EXIT_FAILURE;
    }

    ABinderProcess_joinThreadPool();
    return EXIT_FAILURE;  // joinThreadPool() must not return
}
