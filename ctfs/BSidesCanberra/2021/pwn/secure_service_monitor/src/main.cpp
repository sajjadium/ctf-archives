#include <iostream>
#include <vector>
#include <string>
#include <functional>
#include <mutex>
#include <Winsock2.h>
#include <WS2tcpip.h>
#include <windns.h>
#include <iphlpapi.h>
#include <io.h>
#include <fcntl.h>
#include <windows.h>
#include <limits>
#undef max

extern "C" {
    bool DoTCPCheck(SOCKADDR_IN&);
}

// From https://stackoverflow.com/a/439876
template<typename T>
struct ZeroFreeAllocator : std::allocator<T>
{
    typedef typename std::allocator<T>::pointer pointer;
    typedef typename std::allocator<T>::size_type size_type;

    template<typename U>
    struct rebind
    {
        typedef ZeroFreeAllocator<U> other;
    };

    ZeroFreeAllocator() {}

    template<typename U>
    ZeroFreeAllocator(ZeroFreeAllocator<U> const& u)
        :std::allocator<T>(u) {}

    pointer allocate(size_type size,
        std::allocator<void>::const_pointer = 0)
    {
        void* p = std::malloc(size * sizeof(T));
        if (p == 0)
        {
            throw std::bad_alloc();
        }
        return static_cast<pointer>(p);
    }

    void deallocate(pointer p, size_type size)
    {
        // Zero out freed memory so we don't get any infoleaks
        memset(p, 0x00, size * sizeof(T));
        std::free(p);
    }
};

// Define string types which use our custom allocator to zero out memory when freed
typedef std::basic_string<char, std::char_traits<char>, ZeroFreeAllocator<char>> string;
typedef std::basic_string<wchar_t, std::char_traits<wchar_t>, ZeroFreeAllocator<wchar_t>> wstring;

class Service
{
public:
    Service(string&& name, SOCKADDR_IN& endpoint, std::function<bool(SOCKADDR_IN&)> func)
    {
        m_friendlyName = name;
        m_endpoint = endpoint;
        m_checkFunc = func;
    }

    bool RunCheck()
    {
        if (m_endpoint.sin_family == AF_INET)
        {
            return m_checkFunc(m_endpoint);
        }
        else
        {
            return false;
        }
    }

    auto& GetName()
    {
        return m_friendlyName;
    }

private:
    string m_friendlyName;
    SOCKADDR_IN m_endpoint;
    std::function<bool(SOCKADDR_IN&)> m_checkFunc;
};

class ServiceMonitorApplication
{
public:
    ServiceMonitorApplication();

    void Run();
    void AddService();
    void EditService();
    void ListServices();
    void ListMonitoredServices();
    void DoChecks();

private:
    std::mutex m_servicesMutex;
    std::vector<Service, ZeroFreeAllocator<Service>> m_services;
    std::vector<std::reference_wrapper<Service>, ZeroFreeAllocator<std::reference_wrapper<Service>>> m_monitoredServices;
};

typedef void (ServiceMonitorApplication::* MemberFn)();

const MemberFn appFuncs[] = {
    &ServiceMonitorApplication::AddService,
    &ServiceMonitorApplication::EditService,
    &ServiceMonitorApplication::ListServices,
    &ServiceMonitorApplication::ListMonitoredServices,
    &ServiceMonitorApplication::DoChecks
};

void ReadName(string& str)
{
    // Read until we get a blank line
    char temp[2048];
    str.clear();
    bool first = true;
    while (std::cin.peek() != '\n')
    {
        if (!first)
        {
            str.append("\n");
        }
        std::cin.getline(temp, sizeof(temp));
        str.append(temp);
        first = false;
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

ServiceMonitorApplication::ServiceMonitorApplication()
{
    m_services.reserve(10);
}

void ServiceMonitorApplication::DoChecks()
{
    std::cout << "Running checks..." << std::endl;
    for (Service& service : m_monitoredServices)
    {
        if (!service.RunCheck())
        {
            std::cout << "Check failed for " << service.GetName() << std::endl;
        }
    }
    std::cout << "Checks complete" << std::endl;
}

void ServiceMonitorApplication::AddService()
{
    std::cout << "Service name (end with blank line): ";
    string serviceName;
    ReadName(serviceName);

    std::cout << "Service endpoint: ";
    wstring serviceIP;
    std::getline(std::wcin, serviceIP);

    NET_ADDRESS_INFO addrInfo;
    uint16_t port;
    if (FAILED(ParseNetworkString(serviceIP.c_str(), NET_STRING_IPV4_SERVICE, &addrInfo, &port, nullptr)) || addrInfo.Format != NET_ADDRESS_IPV4)
    {
        std::cout << "Invalid service endpoint" << std::endl;
        return;
    }

    std::cout << "Enable monitoring: ";
    string strEnableMonitoring;
    std::getline(std::cin, strEnableMonitoring);
    bool enableMonitoring = (strEnableMonitoring == "yes" || strEnableMonitoring == "1" || strEnableMonitoring == "y");

    std::lock_guard<std::mutex> lock(m_servicesMutex);
    m_services.emplace_back(std::move(serviceName), addrInfo.Ipv4Address, DoTCPCheck); // TODO: Implement more check functions
    if (enableMonitoring)
    {
        m_monitoredServices.emplace_back(m_services.back());
    }
}

void ServiceMonitorApplication::EditService()
{
    std::cout << "Service number: ";
    size_t serviceNumber;
    std::cin >> serviceNumber;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    std::lock_guard<std::mutex> lock(m_servicesMutex);
    if (serviceNumber > m_services.size() || serviceNumber <= 0)
    {
        std::cout << "Invalid service number" << std::endl;
        return;
    }

    auto& service = m_services[serviceNumber - 1];
    std::cout << "Selected service: " << service.GetName() << std::endl;

    std::cout << "New name (end with blank line): ";
    ReadName(service.GetName());
}

void ServiceMonitorApplication::ListServices()
{
    std::cout << "All services:" << std::endl;

    size_t i = 1;
    std::lock_guard<std::mutex> lock(m_servicesMutex);
    for (auto& service : m_services)
    {
        std::cout << i << ". " << service.GetName() << std::endl;
        i++;
    }
}

void ServiceMonitorApplication::ListMonitoredServices()
{
    std::cout << "Monitored services:" << std::endl;

    size_t i = 1;
    std::lock_guard<std::mutex> lock(m_servicesMutex);
    for (Service& service : m_monitoredServices)
    {
        std::cout << i << ". " << service.GetName() << std::endl;
        i++;
    }
}

void ServiceMonitorApplication::Run()
{
    std::cout << "Welcome to the service monitoring system." << std::endl;

    while (true)
    {
        std::cout << "=== Main Menu ===" << std::endl;
        std::cout << "1. Add a service" << std::endl;
        std::cout << "2. Edit a service" << std::endl;
        std::cout << "3. List services" << std::endl;
        std::cout << "4. List monitored services" << std::endl;
        std::cout << "5. Run checks" << std::endl;
        std::cout << "6. Quit" << std::endl;
        std::cout << "Option: ";

        size_t option;
        std::cin >> option;
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        if (option == (_countof(appFuncs) + 1))
        {
            return;
        }
        else if (option > _countof(appFuncs) || option < 1)
        {
            std::cout << "Invalid option" << std::endl;
        }
        else
        {
            std::invoke(appFuncs[option - 1], this);
        }
    }
}

int main()
{
    _setmode(_fileno(stdout), _O_BINARY);
    setvbuf(stdout, NULL, _IONBF, 0);
    std::cin.exceptions(std::istream::failbit | std::istream::badbit | std::istream::eofbit);
    std::cout.exceptions(std::ostream::failbit | std::ostream::badbit | std::istream::eofbit);

    // Turn on lots of Windows security features so no one can exploit this app
    PROCESS_MITIGATION_IMAGE_LOAD_POLICY imageLoadPolicy = { 0 };
    imageLoadPolicy.NoRemoteImages = 1;
    imageLoadPolicy.NoLowMandatoryLabelImages = 1;
    imageLoadPolicy.PreferSystem32Images = 1;
    if (!SetProcessMitigationPolicy(ProcessImageLoadPolicy, &imageLoadPolicy, sizeof(imageLoadPolicy)))
    {
        std::cout << "Failed to set ProcessImageLoadPolicy" << std::endl;
        return 1;
    }

    PROCESS_MITIGATION_BINARY_SIGNATURE_POLICY signaturePolicy = { 0 };
    signaturePolicy.MicrosoftSignedOnly = 1;
    if (!SetProcessMitigationPolicy(ProcessSignaturePolicy, &signaturePolicy, sizeof(signaturePolicy)))
    {
        std::cout << "Failed to set ProcessSignaturePolicy" << std::endl;
        return 1;
    }

    PROCESS_MITIGATION_DYNAMIC_CODE_POLICY dynamicCodePolicy = { 0 };
    dynamicCodePolicy.ProhibitDynamicCode = 1;
    if (!SetProcessMitigationPolicy(ProcessDynamicCodePolicy, &dynamicCodePolicy, sizeof(dynamicCodePolicy)))
    {
        std::cout << "Failed to set ProcessDynamicCodePolicy" << std::endl;
        return 1;
    }

    PROCESS_MITIGATION_SYSTEM_CALL_DISABLE_POLICY systemCallPolicy = { 0 };
    systemCallPolicy.DisallowWin32kSystemCalls = 1;
    if (!SetProcessMitigationPolicy(ProcessSystemCallDisablePolicy, &systemCallPolicy, sizeof(systemCallPolicy)))
    {
        std::cout << "Failed to set ProcessSystemCallDisablePolicy" << std::endl;
        return 1;
    }

    WSADATA data;
    int result = WSAStartup(MAKEWORD(2, 2), &data);
    if (result != 0)
    {
        std::cout << "WSAStartup failed: " << result << std::endl;
        return 1;
    }

    ServiceMonitorApplication app;
    app.Run();

    WSACleanup();
    return 0;
}
