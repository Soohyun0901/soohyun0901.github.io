# 10. QEMU/KVM 가상머신
QEMU(Quick Emulator의 약자)는 실제 컴퓨터를 에뮬레이션하는 오픈 소스 하이퍼바이저입니다. QEMU가 실행되는 호스트 시스템의 관점에서 볼 때, QEMU는 파티션, 파일, 네트워크 카드와 같은 여러 로컬 리소스에 액세스할 수 있는 사용자 프로그램이며, 이는 에뮬레이션된 컴퓨터로 전달되어 마치 실제 장치인 것처럼 인식됩니다.<br>

에뮬레이션된 컴퓨터에서 실행되는 게스트 운영 체제는 이러한 장치에 액세스하고 실제 하드웨어에서 실행되는 것처럼 실행합니다. 예를 들어 ISO 이미지를 QEMU에 매개변수로 전달하면 에뮬레이션된 컴퓨터에서 실행되는 OS는 CD 드라이브에 삽입된 실제 CD-ROM을 인식합니다.<br>

QEMU는 ARM에서 Sparc에 이르기까지 다양한 하드웨어를 에뮬레이션할 수 있지만, Proxmox VE는 압도적인 대다수의 서버 하드웨어를 나타내기 때문에 32비트 및 64비트 PC 클론 에뮬레이션에만 관심이 있습니다. PC 클론의 에뮬레이션은 에뮬레이션된 아키텍처가 호스트 아키텍처와 동일할 때 QEMU를 크게 가속화하는 프로세서 확장의 가용성으로 인해 가장 빠른 것 중 하나입니다.

> ![](../_static/img/bell.png) <span class="point">KVM</span>(커널 기반 가상 머신)이라는 용어를 가끔 접할 수 있습니다. 이는 QEMU가 Linux KVM 모듈을 통해 가상화 프로세서 확장의 지원으로 실행 중임을 의미합니다. Proxmox VE의 맥락에서 <span class="point">QEMU</span>와 <span class="point">KVM</span>은 상호 교환하여 사용할 수 있습니다. Proxmox VE의 QEMU는 항상 KVM 모듈을 로드하려고 시도합니다.
Proxmox VE 내부의 QEMU는 블록 및 PCI 장치에 액세스하는 데 필요하므로 루트 프로세스로 실행됩니다.<br><br>

## 10.1. 에뮬레이션된 장치와 준가상화 장치
QEMU에서 에뮬레이션한 PC 하드웨어에는 마더보드, 네트워크 컨트롤러, SCSI, IDE 및 SATA 컨트롤러, 직렬 포트(전체 목록은 kvm(1) 매뉴얼 페이지에서 볼 수 있음)가 포함되며, 이 모든 것이 소프트웨어에서 에뮬레이션됩니다. 이러한 모든 장치는 기존 하드웨어 장치와 정확히 동일한 소프트웨어이며, 게스트에서 실행되는 OS에 적절한 드라이버가 있는 경우 실제 하드웨어에서 실행되는 것처럼 장치를 사용합니다. 이를 통해 QEMU는 <span class="point">수정되지 않은 운영 체제</span>를 실행할 수 있습니다.<br>

그러나 이는 성능 비용이 발생합니다. 하드웨어에서 실행되도록 의도된 것을 소프트웨어에서 실행하면 호스트 CPU에 많은 추가 작업이 필요합니다. 이를 완화하기 위해 QEMU는 게스트 운영 체제에 <span class="point">준가상화 장치</span>를 제공할 수 있으며, 게스트 OS는 QEMU 내부에서 실행 중임을 인식하고 하이퍼바이저와 협력합니다.<br>

QEMU는 virtio 가상화 표준에 의존하며, 따라서 paravirtio 장치를 제공할 수 있습니다. 여기에는 paravirtio 일반 디스크 컨트롤러, paravirtio 네트워크 카드, paravirtio 직렬 포트, paravirtio SCSI 컨트롤러 등이 포함됩니다.

>> ![](../_static/img/bell.png) virtio 장치는 성능이 크게 향상되고 일반적으로 유지 관리가 더 잘 되므로 <span class="point">가능한 한</span> 사용하는 것이 좋습니다. virtio 일반 디스크 컨트롤러를 에뮬레이트된 IDE 컨트롤러와 비교하면 <span class="point">bonnie++(8)</span>로 측정한 순차 쓰기 처리량이 두 배가 됩니다. virtio 네트워크 인터페이스를 사용하면 <span class="point">iperf(1)</span>로 측정한 에뮬레이트된 Intel E1000 네트워크 카드보다 최대 3배의 처리량을 제공할 수 있습니다. 

<br><br>

## 10.2. 가상 머신 설정
일반적으로 Proxmox VE는 가상 머신(VM)에 대해 건전한 기본값을 선택하려고 합니다. 변경하는 설정의 의미를 이해해야 합니다. 성능이 저하되거나 데이터가 위험에 처할 수 있습니다.

### 10.2.1. 일반 설정
![](../_static/img/img46.png)<br>
VM의 일반 설정은 다음과 같습니다.

- <span class="point">Node</span>
    - 

- <span class="point">VM ID</span>
    - 이 Proxmox VE 설치에서 VM을 식별하는 데 사용되는 고유 번호

- <span class="point">Name</span>
    - VM을 설명하는 데 사용할 수 있는 자유 형식 텍스트 문자열

- <span class="point">Resource Pool</span>
    - VM의 논리적 그룹

<br><br>

### 10.2.2. OS 설정
![](../_static/img/img47.png)<br>
가상 머신(VM)을 생성할 때 적절한 운영 체제(OS)를 설정하면 Proxmox VE가 일부 저수준 매개변수를 최적화할 수 있습니다. 예를 들어 Windows OS는 BIOS 시계가 로컬 시간을 사용하기를 기대하는 반면, Unix 기반 OS는 BIOS 시계가 UTC 시간을 사용하기를 기대합니다.<br>
### 10.2.3. 시스템 설정
![](../_static/img/img48.png)<br>
VM을 생성할 때 새 VM의 일부 기본 시스템 구성 요소를 변경할 수 있습니다. 사용할 디스플레이 유형을 지정할 수 있습니다.<br>
또한 SCSI 컨트롤러를 변경할 수 있습니다. QEMU 게스트 에이전트를 설치할 계획이거나 선택한 ISO 이미지가 이미 제공되어 자동으로 설치되는 경우 <span class="point">QEMU Agent</span> 상자를 선택하여 Proxmox VE가 해당 기능을 사용하여 더 많은 정보를 표시하고 일부 작업(예: 종료 또는 스냅샷)을 보다 지능적으로 완료할 수 있음을 알릴 수 있습니다.<br>

Proxmox VE는 SeaBIOS 및 OVMF와 같은 다양한 펌웨어 및 머신 유형으로 VM을 부팅할 수 있습니다. 대부분의 경우 PCIe 패스스루를 사용할 계획인 경우에만 기본 SeaBIOS에서 OVMF로 전환합니다.<br><br>

<span class="point">![](../_static/img/info.png) 머신 유형</span><br>
VM의 <span class="point">머신 유형</span>은 VM의 가상 마더보드의 하드웨어 레이아웃을 정의합니다. 기본 Intel 440FX 또는 Q35 칩셋 중에서 선택할 수 있습니다. Q35 칩셋은 가상 PCIe 버스도 제공하므로 PCIe 하드웨어를 통과하려는 경우 바람직할 수 있습니다. 또한 vIOMMU 구현을 선택할 수 있습니다.<br><br>

<span class="point">![](../_static/img/info.png) 머신 버전</span><br>
각 머신 유형은 QEMU에서 버전이 지정되고 주어진 QEMU 바이너리는 여러 머신 버전을 지원합니다. 새 버전은 새로운 기능, 수정 사항 또는 일반적인 개선 사항에 대한 지원을 제공할 수 있습니다. 그러나 가상 하드웨어의 속성도 변경합니다. 게스트 관점에서 갑작스러운 변경을 방지하고 VM 상태의 호환성을 보장하기 위해 라이브 마이그레이션 및 RAM 스냅샷은 새 QEMU 인스턴스에서 동일한 머신 버전을 계속 사용합니다.<br>

Windows 게스트의 경우 머신 버전은 생성 중에 고정됩니다. Windows는 콜드 부팅 간에도 가상 하드웨어의 변경 사항에 민감하기 때문입니다. 예를 들어, 네트워크 장치의 열거는 머신 버전마다 다를 수 있습니다. Linux와 같은 다른 OS는 일반적으로 이러한 변경 사항을 잘 처리할 수 있습니다. 이러한 경우 <span class="point">최신 머신 버전</span>이 기본적으로 사용됩니다. 즉, 새로 시작한 후에는 QEMU 바이너리에서 지원하는 최신 머신 버전이 사용됩니다(예: QEMU 8.1이 지원하는 최신 머신 버전은 각 머신 유형에 대해 버전 8.1입니다).<br><br>

<span class="point">![](../_static/img/info.png) 최신 머신 버전으로 업데이트</span><br>
매우 오래된 머신 버전은 QEMU에서 더 이상 지원되지 않을 수 있습니다. 예를 들어, i440fx 머신 유형의 버전 1.4~1.7이 해당합니다. 이러한 머신 버전에 대한 지원은 언젠가 중단될 것으로 예상됩니다. 지원 중단 경고가 표시되면 머신 버전을 최신 버전으로 변경해야 합니다. 먼저 작동하는 백업을 만들고 게스트가 하드웨어를 보는 방식이 변경될 수 있으므로 대비하세요. 어떤 경우에는 특정 드라이버를 다시 설치해야 할 수도 있습니다. 이러한 머신 버전으로 찍은 RAM이 있는 스냅샷도 확인해야 합니다(예: <span class="point">runningmachine</span> 구성 항목). 안타깝게도 스냅샷의 머신 버전을 변경할 방법이 없으므로 스냅샷을 로드하여 데이터를 복구해야 합니다.<br><br>

### 10.2.4. 하드디스크
<span class="point">![](../_static/img/info.png) 버스/컨트롤러</span><br>
QEMU는 여러 스토리지 컨트롤러를 에뮬레이션할 수 있습니다.

> ![](../_static/img/bell.png) 성능상의 이유와 더 나은 유지 관리를 위해 <span class="point">VirtIO SCSI</span> 또는 <span class="point">VirtIO Block</span> 컨트롤러를 사용하는 것이 좋습니다.

- <span class="point">IDE</span> 컨트롤러는 1984년 PC/AT 디스크 컨트롤러로 거슬러 올라가는 디자인을 가지고 있습니다. 이 컨트롤러가 최근 디자인으로 대체되었더라도 생각할 수 있는 모든 OS가 이를 지원하므로 2003년 이전에 출시된 OS를 실행하려는 경우 좋은 선택입니다. 이 컨트롤러에 최대 4개의 장치를 연결할 수 있습니다.

- 2003년의 <span class="point">SATA</span>(Serial ATA) 컨트롤러는 보다 현대적인 디자인을 가지고 있어 더 높은 처리량과 더 많은 수의 장치를 연결할 수 있습니다. 이 컨트롤러에 최대 6개의 장치를 연결할 수 있습니다.

- 1985년에 설계된 <span class="point">SCSI</span> 컨트롤러는 일반적으로 서버 등급 하드웨어에서 발견되며 최대 14개의 스토리지 장치를 연결할 수 있습니다. Proxmox VE는 기본적으로 LSI 53C895A 컨트롤러를 에뮬레이션합니다.

- 성능을 목표로 하는 경우 <span class="point">VirtIO SCSI single</span> 유형의 SCSI 컨트롤러를 사용하고 연결된 디스크에 대한 IO 스레드 설정을 활성화하는 것이 좋습니다. 이는 Proxmox VE 7.3 이후 새로 생성된 Linux VM의 기본값입니다. 각 디스크에는 고유한 <span class="point">VirtIO SCSI </span>컨트롤러가 있으며 QEMU는 전용 스레드에서 디스크 IO를 처리합니다. Linux 배포판은 2012년부터 이 컨트롤러를 지원했고 FreeBSD는 2014년부터 지원했습니다. Windows OS의 경우 설치 중에 드라이버가 포함된 추가 ISO를 제공해야 합니다.

- <span class="point">VirtIO Block</span> 컨트롤러는 종종 VirtIO 또는 virtio-blk라고 불리며, 이전 유형의 준가상화 컨트롤러입니다. 기능 면에서 VirtIO SCSI 컨트롤러로 대체되었습니다.

<br><br>

<span class="point">![](../_static/img/info.png) 이미지 형식</span><br>
각 컨트롤러에서 여러 에뮬레이션된 하드 디스크를 연결하는데, 이 디스크는 구성된 스토리지에 있는 파일이나 블록 디바이스로 백업됩니다. 스토리지 유형을 선택하면 하드 디스크 이미지의 형식이 결정됩니다. 블록 디바이스(LVM, ZFS, Ceph)를 제공하는 스토리지는 <span class="point">원시 디스크 이미지 형식</span>이 필요한 반면, 파일 기반 스토리지(Ext4, NFS, CIFS, GlusterFS)는 <span class="point">원시 디스크 이미지 형식</span>이나 <span class="point">QEMU 이미지 형식</span>을 선택할 수 있습니다.

- <span class="point">QEMU 이미지 형식</span>은 스냅샷과 디스크 이미지의 씬 프로비저닝을 허용하는 쓰기 시 복사 형식입니다.

- <span class="point">원시 디스크 이미지</span>는 Linux에서 블록 디바이스에서 <span class="point">dd</span> 명령을 실행할 때 얻는 것과 유사한 하드 디스크의 비트 대 비트 이미지입니다. 이 형식은 씬 프로비저닝이나 스냅샷을 자체적으로 지원하지 않으므로 이러한 작업을 위해 스토리지 계층의 협조가 필요합니다. 그러나 <span class="point">QEMU 이미지 형식</span>보다 최대 10% 더 빠를 수 있습니다. 

- <span class="point">VMware 이미지 형식</span>은 디스크 이미지를 다른 하이퍼바이저로 가져오거나 내보내려는 경우에만 의미가 있습니다.

<br><br>
<span class="point">![](../_static/img/info.png) 캐시 모드</span><br>
하드 드라이브의 <span class="point">캐시(Cache)</span> 모드를 설정하면 호스트 시스템이 게스트 시스템에 블록 쓰기 완료를 알리는 방식에 영향을 미칩니다. <span class="point">캐시 없음(No Cache)</span> 기본값은 각 블록이 물리적 스토리지 쓰기 대기열에 도달하면 게스트 시스템에 쓰기가 완료되었다는 알림이 전송되고 호스트 페이지 캐시는 무시된다는 것을 의미합니다. 이는 안전성과 속도 간의 적절한 균형을 제공합니다.<br>

Proxmox VE 백업 관리자가 VM 백업을 수행할 때 디스크를 건너뛰게 하려면 해당 디스크에서 <span class="point">백업 없음(No backup)</span> 옵션을 설정할 수 있습니다.<br>

Proxmox VE 스토리지 복제 메커니즘이 복제 작업을 시작할 때 디스크를 건너뛰게 하려면 해당 디스크에서 <span class="point">복제 건너뛰기(Skip replication)</span> 옵션을 설정할 수 있습니다. Proxmox VE 5.0부터 복제에는 디스크 이미지가 <span class="point">zfspool</span> 유형의 스토리지에 있어야 하므로 VM에 복제가 구성된 경우 다른 스토리지에 디스크 이미지를 추가하려면 이 디스크 이미지에 대한 복제를 건너뛰어야 합니다.<br><br>
<span class="point">![](../_static/img/info.png) Trim/Discard</span><br>
스토리지가 <span class="point">씬 프로비저닝</span>을 지원하는 경우(Proxmox VE 가이드의 스토리지 챕터 참조) 드라이브에서 <span class="point">Discard</span> 옵션을 활성화할 수 있습니다. <span class="point">Discard</span>가 설정되고 <span class="point">TRIM</span>이 활성화된 게스트 OS가 있는 경우 VM의 파일 시스템이 파일을 삭제한 후 블록을 사용하지 않는 것으로 표시하면 컨트롤러가 이 정보를 스토리지로 전달하여 디스크 이미지를 그에 따라 축소합니다. 게스트가 <span class="point">TRIM</span> 명령을 실행할 수 있도록 하려면 드라이브에서 <span class="point">Discard</span> 옵션을 활성화해야 합니다. 일부 게스트 운영 체제에서는 <span class="point">SSD 에뮬레이션</span> 플래그를 설정해야 할 수도 있습니다. <span class="point">VirtIO Block</span> 드라이브에서 <span class="point">Discard</span>는 Linux Kernel 5.0 이상을 사용하는 게스트에서만 지원됩니다.<br>

드라이브를 회전형 하드 디스크가 아닌 솔리드 스테이트 드라이브로 게스트에게 표시하려면 해당 드라이브에서 <span class="point">SSD 에뮬레이션</span> 옵션을 설정할 수 있습니다. 기본 스토리지가 실제로 SSD로 백업되어야 한다는 요구 사항은 없습니다. 이 기능은 모든 유형의 물리적 미디어에서 사용할 수 있습니다. <span class="point">VirtIO Block</span> 드라이브에서는 <span class="point">SSD 에뮬레이션</span>이 지원되지 않습니다.<br><br>

<span class="point">![](../_static/img/info.png) IO 스레드</span><br>
<span class="point">IO 스레드</span> 옵션은 <span class="point">VirtIO</span> 컨트롤러가 있는 디스크를 사용하거나 에뮬레이트된 컨트롤러 유형이 <span class="point">VirtIO SCSI single</span>인 <span class="point">SCSI</span> 컨트롤러가 있는 경우에만 사용할 수 있습니다. <span class="point">IO 스레드</span>가 활성화되면 QEMU는 기본 이벤트 루프 또는 vCPU 스레드에서 모든 I/O를 처리하는 대신 스토리지 컨트롤러당 하나의 I/O 스레드를 만듭니다. 한 가지 이점은 기본 스토리지의 더 나은 작업 분배 및 활용입니다. 또 다른 이점은 메인 스레드나 vCPU 스레드가 디스크 I/O에 의해 차단될 수 없기 때문에 매우 I/O 집약적인 호스트 작업 부하에 대한 게스트의 대기 시간(멈춤)이 줄어드는 것입니다.<br><br>

### 10.2.5. CPU
![](../_static/img/img49.png)<br>

<span class="point">CPU 소켓</span>은 CPU를 연결할 수 있는 PC 마더보드의 실제 슬롯입니다. 이 CPU는 독립적인 처리 장치인 하나 이상의 <span class="point">코어</span>를 포함할 수 있습니다. 4개의 코어가 있는 단일 CPU 소켓이든 2개의 코어가 있는 2개의 CPU 소켓이든 성능 관점에서는 대부분 중요하지 않습니다. 그러나 일부 소프트웨어 라이선스는 머신의 소켓 수에 따라 달라지므로 이 경우 라이선스에서 허용하는 소켓 수를 설정하는 것이 합리적입니다.<br>

가상 CPU(코어 및 소켓) 수를 늘리면 일반적으로 성능이 향상되지만 이는 VM 사용에 크게 좌우됩니다. 멀티스레드 애플리케이션은 물론 많은 수의 가상 CPU에서 이점을 얻을 수 있습니다. 추가하는 각 가상 CPU에 대해 QEMU는 호스트 시스템에 새 실행 스레드를 만들기 때문입니다. VM의 작업 부하에 대해 확신이 없다면 일반적으로 <span class="point">총 코어 수</span>를 2로 설정하는 것이 안전합니다.

> ![](../_static/img/bell.png) 모든 VM의 전체 코어 수가 서버의 코어 수보다 큰 경우(예: 코어가 8개인 머신에서 각각 코어가 4개인 VM 4개(= 총 16개)) 완벽하게 안전합니다. 이 경우 호스트 시스템은 표준 멀티스레드 애플리케이션을 실행하는 것처럼 서버 코어 간에 QEMU 실행 스레드를 균형 있게 조정합니다. 그러나 Proxmox VE는 물리적으로 사용 가능한 것보다 더 많은 가상 CPU 코어가 있는 VM을 시작하지 못하게 합니다. 컨텍스트 전환 비용으로 인해 성능이 저하될 뿐입니다.<br><br>

<span class="point">![](../_static/img/info.png) 리소스 제한</span><br>
<span class="point">☑︎ cpulimit</span>

가상 코어 수 외에도 VM에 사용 가능한 총 "호스트 CPU 시간"을 <span class="point">cpulimit</span> 옵션으로 설정할 수 있습니다. CPU 시간을 백분율로 나타낸 부동 소수점 값이므로 <span class="point">1.0</span>은 <span class="point">100%</span>, <span class="point">2.5</span>는 <span class="point">250%</span>와 같습니다. 단일 프로세스가 단일 코어 하나를 완전히 사용하면 CPU 시간 사용량이 <span class="point">100%</span>가 됩니다. 코어가 4개인 VM이 모든 코어를 완전히 활용하면 이론적으로 <span class="point">400%</span>가 됩니다. 실제로는 QEMU가 vCPU 코어 외에 VM 주변 장치에 대한 추가 스레드를 가질 수 있으므로 사용량이 조금 더 높을 수 있습니다.<br>

이 설정은 VM이 일부 프로세스를 병렬로 실행하기 때문에 여러 vCPU가 있어야 하지만 VM 전체가 모든 vCPU를 동시에 100%로 실행할 수 없는 경우에 유용할 수 있습니다.<br>

예를 들어, 8개의 가상 CPU가 있으면 도움이 되는 가상 머신이 있지만, VM이 모든 8개 코어를 전체 부하로 실행하여 최대로 사용할 수 있기를 원하지 않는 경우를 가정해 보겠습니다. 그러면 서버에 과부하가 걸리고 다른 가상 머신과 컨테이너에 CPU 시간이 너무 적게 남게 됩니다. 이를 해결하려면 <span class="point">cpulimit</span>을 <span class="point">4.0(=400%)</span>으로 설정할 수 있습니다. 즉, VM이 8개 프로세스를 동시에 실행하여 모든 8개 가상 CPU를 완전히 활용하면 각 vCPU는 물리적 코어에서 최대 50%의 CPU 시간을 받습니다. 그러나 VM 워크로드가 4개의 가상 CPU만 완전히 활용하면 물리적 코어에서 최대 100%의 CPU 시간을 받을 수 있어 총 400%가 됩니다.

> ![](../_static/img/bell.png) VM은 구성에 따라 네트워킹이나 IO 작업과 같은 추가 스레드를 사용할 수 있지만 라이브 마이그레이션도 가능합니다. 따라서 VM은 가상 CPU만이 사용할 수 있는 것보다 더 많은 CPU 시간을 사용할 수 있습니다. VM이 할당된 vCPU보다 더 많은 CPU 시간을 사용하지 않도록 하려면 <span class="point">cpulimit</span>을 총 코어 수와 동일한 값으로 설정합니다.

<br><br>

cpuunits

cpuunits 옵션을 사용하면 요즘은 CPU 공유 또는 CPU 가중치라고도 하며, 실행 중인 다른 VM과 비교하여 VM이 얻는 CPU 시간을 제어할 수 있습니다. 이는 상대적 가중치로, 기본값은 100(또는 호스트가 레거시 cgroup v1을 사용하는 경우 1024)입니다. VM에 대해 이 값을 늘리면 스케줄러가 가중치가 낮은 다른 VM과 비교하여 우선순위를 지정합니다.

예를 들어 VM 100이 기본값인 100을 설정하고 VM 200을 200으로 변경한 경우, 후자의 VM 200은 첫 번째 VM 100보다 두 배의 CPU 대역폭을 받습니다.

자세한 내용은 man systemd.resource-control을 참조하세요. 여기서 CPUQuota는 cpulimit에 해당하고 CPUWeight는 cpuunits 설정에 해당합니다. 참조 및 구현 세부 정보는 참고 사항 섹션을 참조하세요.

affinity

affinity 옵션을 사용하면 VM의 vCPU를 실행하는 데 사용되는 실제 CPU 코어를 지정할 수 있습니다. I/O와 같은 주변 VM 프로세스는 이 설정의 영향을 받지 않습니다. CPU 친화성은 보안 기능이 아니라는 점에 유의하세요.

CPU 친화성을 강제하는 것은 특정 경우에 의미가 있을 수 있지만 복잡성과 유지 관리 노력이 증가합니다. 예를 들어 나중에 더 많은 VM을 추가하거나 VM을 CPU 코어가 적은 노드로 마이그레이션하려는 경우입니다. 일부 CPU가 완전히 활용되는 반면 다른 CPU는 거의 유휴 상태인 경우 비동기적이고 따라서 시스템 성능이 제한될 수도 있습니다.

친화성은 taskset CLI 도구를 통해 설정됩니다. man cpuset의 목록 형식에서 호스트 CPU 번호(lscpu 참조)를 허용합니다. 이 ASCII 10진수 목록에는 숫자뿐만 아니라 숫자 범위도 포함될 수 있습니다. 예를 들어 친화성 0-1,8-11(확장된 0, 1, 8, 9, 10, 11)은 VM이 이 6개의 특정 호스트 코어에서만 실행되도록 허용합니다.

