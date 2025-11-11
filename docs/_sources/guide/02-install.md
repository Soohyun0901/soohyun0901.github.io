# 2. Proxmox VE 기본설치

Proxmox VE는 Debian Linux를 기반으로 합니다. 그렇기 때문에 Proxmox에서 제공하는 설치 디스크 이미지(ISO 파일)에는 전체 Debian 시스템과 필요한 모든 Proxmox VE 패키지가 포함되어 있습니다.<br>
> ![](../_static/images/pin.png) Proxmox VE 릴리스와 Debian 릴리스 간의 관계는 FAQ의 지원 표를 참조하세요.

설치 관리자는 로컬 디스크를 파티션하고, 기본 시스템 구성(예: 시간대, 언어, 네트워크)을 적용하고, 필요한 모든 패키지를 설치할 수 있도록 설정 과정을 안내합니다. 이 과정은 몇 분 이상 소요되지 않습니다. 신규 및 기존 사용자에게는 제공된 ISO로 설치하는 것이 권장됩니다.<br>
또는 기존 Debian 시스템 위에 Proxmox VE를 설치할 수도 있습니다. 이 옵션은 Proxmox VE에 대한 자세한 지식이 필요하므로 고급 사용자에게만 권장됩니다.<br><br>

##  2.1. 시스템 요구사항
프로덕션 환경에서 Proxmox VE를 실행할 때는 고품질 서버 하드웨어를 사용하는 것이 좋습니다. 호스트 장애의 영향을 더욱 줄이기 위해, 고가용성(HA) 가상 머신 및 컨테이너가 있는 클러스터에서 Proxmox VE를 실행할 수 있습니다.<br>

Proxmox VE는 로컬 스토리지(DAS), SAN, NAS 및 Ceph RBD와 같은 분산 스토리지를 사용할 수 있습니다. 자세한 내용은 스토리지 챕터를 참조하세요.<br><br>

### 2.1.1. 테스트를 위한 최소 요구사항

이러한 최소 요구사항은 오직 테스트 목적으로만 사용되어야 하며, 프로덕션 환경에 사용해서는 안 됩니다.
* CPU: 64비트(Intel 64 또는 AMD64)
* KVM 전체 가상화 지원을 위한 Intel VT/AMD-V 지원 CPU/마더보드
* RAM: 1GB RAM, 게스트를 위한 추가 RAM
* 하드 드라이브
* 네트워크 카드(NIC) 1개<br><br>

### 2.1.2. 권장 시스템 요구사항

* Intel 64 또는 AMD64(Intel VT/AMD-V CPU 플래그 포함)
* 메모리: OS 및 Proxmox VE 서비스용 최소 2GB, 추가 게스트용 지정 메모리, Ceph와 ZFS의 경우, 사용 중인 스토리지 1TB당 약 1GB의 메모리가 추가로 필요합니다.
* 빠르고 이중화된 스토리지(SSD를 사용하면 최상의 결과를 얻을 수 있습니다.)
* OS 스토리지: 배터리 보호 쓰기 캐시(BBU)가 있는 하드웨어 RAID 또는 ZFS(ZIL의 경우 SSD 옵션)가 있는 비 RAID를 사용 권장
* VM 스토리지:
  - 로컬 스토리지의 경우, 배터리 백업 쓰기 캐시(BBU)가 있는 하드웨어 RAID를 사용하거나 ZFS 및 Ceph의 경우 비 RAID를 사용합니다. ZFS나 Ceph는 하드웨어 RAID 컨트롤러와 호환되지 않습니다.
  - 공유 및 분산 스토리지가 가능합니다.
  - 우수한 성능을 위해서는 전력 손실 보호(PLP) 기능이 있는 SSD를 사용하는 것이 좋습니다. 일반 소비자용 SSD는 사용하지 않는 것이 좋습니다.
* 선호하는 스토리지 기술 및 클러스터 설정에 따라 추가 NIC가 있는 이중화(멀티) Gbit NIC
* PCI(e) 패스스루의 경우 CPU가 VT-d/AMD-d 플래그를 지원해야 합니다.<br><br>

### 2.1.3. 간단한 성능 개요

설치된 Proxmox VE 시스템에서 CPU 및 하드 디스크 성능에 대한 개요를 확인하려면 포함된 <point>pveperf</point>도구를 실행하세요.

> ![](../_static/images/pin.png) 중요<br>
> 이것은 매우 빠르고 일반적인 벤치마크일 뿐이며, 특히 시스템의 I/O 성능에 대해서는 더 자세한 테스트가 권장됩니다.

### 2.1.4. 웹 인터페이스 액세스를 위해 지원되는 웹 브라우저 

웹 기반 사용자 인터페이스에 액세스하려면 다음 브라우저 중 하나를 사용하는 것이 좋습니다:
* <point>Firefox</point> : 현재 연도의 릴리스 또는 최신 확장 지원 릴리스
* <point>Chrome</point> : 현재 연도의 릴리스
* <point>Microsoft Edge</point> : 현재 지원되는 버전
* <point>Safari</point> : 현재 연도의 릴리스

모바일 장치에서 액세스하는 경우 Proxmox VE는 가벼운 터치 기반 인터페이스를 표시합니다.<br><br>

## 2.2. 설치 미디어 준비

다음 링크에서 설치 프로그램 ISO 이미지를 다운로드하세요:
* ISO 다운로드 URL : [Proxmox VE ISO Installer](https://www.proxmox.com/en/downloads/proxmox-virtual-environment/iso){.highlight-link}
<br>

Proxmox VE 설치 미디어는 하이브리드 ISO 이미지이며, 두 가지 방식으로 작동합니다:

* CD 또는 DVD에 구울 준비가 된 ISO 이미지 파일.
* USB 플래시 드라이브(USB 스틱)에 복사할 준비가 된 원시 섹터(IMG) 이미지 파일.

<br>
USB 플래시 드라이브를 사용하는 것이 더 빠른 옵션이므로 Proxmox VE를 설치하는 데 권장되는 방법입니다.<br><br>

### 2.2.1. 설치 미디어로 USB 플래시 드라이브 준비 
플래시 드라이브에는 최소 1GB의 저장 공간이 있어야 합니다.

> UNetbootin을 사용하지 마십시오. Proxmox VE 설치 이미지에서는 작동하지 않습니다.

<br><br>

### 2.2.2.GNU/Linux용 지침 
유닉스 계열 운영 체제에서는 <point>dd</point> 명령을 사용하여 ISO 이미지를 USB 플래시 드라이브에 복사합니다. 먼저 USB 플래시 드라이브의 올바른 장치 이름을 찾습니다(아래 참조). 그런 다음 <point>dd</point> 명령을 실행합니다.

```
# dd bs=1M conv=fdatasync if=./proxmox-ve_*.iso of=/dev/XYZ
```

dev/XYZ를 올바른 장치 이름으로 바꾸고 입력 파일 이름(<point>if</point>) 경로를 조정해야 합니다.<br><br>

![](../_static/images/pin.png) 올바른 USB 장치 이름 찾기<br>
USB 플래시 드라이브의 이름을 찾는 방법에는 두 가지가 있습니다. 첫 번째는 플래시 드라이브를 연결하기 전과 연결한 후의 <point>dmesg</point> 명령 출력의 마지막 줄을 비교하는 것입니다. 두 번째 방법은 <point>lsblk</point> 명령의 출력을 비교하는 것입니다. 터미널을 열고 실행합니다:

```
# lsblk
```
그런 다음 USB 플래시 드라이브를 연결하고 명령을 다시 실행합니다:

```
# lsblk
```
새 장치가 나타납니다. 이 장치를 사용하세요. 안전을 위해 출력된 크기가 USB 플래시 드라이브와 일치하는지 확인하세요.<br><br>

## 2.3. Proxmox VE 설치 프로그램 시작

Proxmox VE 설치 프로그램 ISO 이미지에는 다음과 같은 요소가 포함되어 있습니다:<br>
* 전체 운영 체제(Debian Linux, 64비트)
* ext4, XFS, BTRFS 또는 ZFS로 로컬 디스크를 파티션하고 운영 체제를 설치하는 Proxmox VE 설치 프로그램
* KVM 및 LXC를 지원하는 Proxmox VE Linux 커널
* 가상 머신, 컨테이너, 호스트 시스템, 클러스터 및 필요한 모든 리소스를 관리하기 위한 완벽한 툴 세트
* 웹 기반 관리 인터페이스

> ![](../_static/images/pin.png) 중요<br>
> 선택한 드라이브의 모든 기존 데이터는 설치 과정에서 제거됩니다. 설치 프로그램은 다른 운영 체제에 대한 부팅 메뉴 항목을 추가하지 않습니다.

준비된 설치 미디어(예: USB 플래시 드라이브 또는 CD-ROM)를 삽입하고 부팅하세요.

> ![](../_static/images/pin.png) 중요<br>
> 서버의 펌웨어 설정에서 설치 미디어(예: USB)에서 부팅이 활성화되어 있는지 확인하세요. Proxmox VE 버전 8.1 이전 설치 관리자를 부팅할 때는 보안 부팅을 비활성화해야 합니다.

<br><br>

### 2.3.1. 설치 모드 선택
<!-- 사진첨부 -->

부팅이 시작되면 Proxmox VE 메뉴가 표시되고 다음 옵션 중 하나를 선택할 수 있습니다:
* <point>Install Proxmox VE(Graphical)</point>
  * 일반 설치를 시작합니다.
* <point>Install Proxmox VE(Terminal UI)</point>
  * 터미널 모드 설치 프로그램을 시작합니다. 
  * 그래픽 설치 프로그램과 동일한 전반적인 설치 환경을 제공하지만 일반적으로 구형 및 최신 하드웨어와의 호환성이 더 우수합니다.
* <point>Install Proxmox VE(Terminal UI, Serial Console)</point>
  * 터미널 모드 설치 프로그램을 시작하고, 추가로 머신의 (첫 번째) 직렬 포트를 입출력용으로 사용하도록 Linux 커널을 설정합니다. 
  * 머신이 완전히 헤드리스이고 직렬 콘솔만 사용할 수 있는 경우 이 옵션을 사용할 수 있습니다.
<!-- 사진첨부 -->
두 모드 모두 실제 설치 프로세스에 동일한 코드 기반을 사용하여 10년 이상의 버그 수정의 이점을 누리고 기능의 동등성을 보장합니다.

> ![](../_static/images/pin.png) 중요<br>
> <point>Terminal UI</point> 옵션은 드라이버 문제 등으로 인해 그래픽 설치가 제대로 작동하지 않는 경우에 사용할 수 있습니다.<br> nomodeset 커널 매개변수 추가도 참조하세요.

* <point>Advanced Options: Install Proxmox VE (Graphical, Debug Mode)</point>
  * 디버그 모드에서 설치를 시작합니다. 여러 설치 단계에서 콘솔이 열리며, 이는 문제가 발생할 경우 상황을 디버깅하는 데 도움이 됩니다. 
  * 디버그 콘솔을 종료하려면 <point>CTRL-D</point>를 누릅니다. 이 옵션은 사용 가능한 모든 기본 도구가 있는 라이브 시스템을 부팅하는 데 사용할 수 있습니다. 예를 들어 이 옵션을 사용하여 성능 저하된 ZFS rpool을 복구하거나 기존 Proxmox VE 설정의 부트 로더를 수정할 수 있습니다.
* <point>Advanced Options: Install Proxmox VE (Terminal UI, Debug Mode)</point>
  * 그래픽 디버그 모드와 동일하지만 대신 터미널 기반 설치 프로그램을 실행할 수 있도록 시스템을 준비합니다.
* <point>Advanced Options: Install Proxmox VE (Serial Console Debug Mode)</point>
  * 터미널 기반 디버그 모드와 동일하지만 추가로 Linux 커널이 머신의 (첫 번째) 직렬 포트를 입출력에 사용하도록 설정합니다.
* <point>Advanced Options: Install Proxmox VE (Automated)</point>
  * ISO가 자동 설치를 위해 적절하게 준비되지 않은 경우에도 무인 모드에서 설치 프로그램을 시작합니다. 
  * 이 옵션은 하드웨어 세부 정보를 수집하는 데 사용하거나 자동 설치 설정을 디버깅하는 데 유용할 수 있습니다. 
* <point>Advanced Options: Rescue Boot</point>
  * 이 옵션을 사용하면 기존 설치를 부팅할 수 있습니다. 
  * 연결된 모든 하드 디스크를 검색합니다. 기존 설치가 발견되면 ISO의 Linux 커널을 사용하여 해당 디스크로 직접 부팅합니다. 
  * 이 옵션은 부트 로더(GRUB/systemd-boot)에 문제가 있거나 BIOS/UEFI가 디스크에서 부팅 블록을 읽을 수 없는 경우에 유용할 수 있습니다.
* <point>Advanced Options: Test Memory (memtest86+)</point>
  * memtest86+를 실행합니다. 메모리가 제대로 작동하고 오류가 없는지 확인하는 데 유용합니다. 
  * 이 옵션을 실행하려면 UEFI 펌웨어 설정 유틸리티에서 보안 부팅이 꺼져 있어야 합니다.
<br>

일반적으로 `Install Proxmox VE (Graphical)`를 선택하여 그래픽 모드로 설치를 진행합니다.

<br><br>

### 2.3.2. 라이선스 확인
첫 번째 단계는 EULA(최종 사용자 라이선스 계약)를 읽는 것입니다.<br>그런 다음 설치 대상 하드 디스크를 선택할 수 있습니다.<br><br><br>

### 2.3.3.하드디스크 선택
<!-- 사진첨부 -->

> ![](../_static/images/pin.png) 중요<br>
> 기본적으로 서버 전체가 사용되며 기존의 모든 데이터가 제거됩니다. 설치를 진행하기 전에 서버에 중요한 데이터가 없는지 확인하세요.

<point>Options</point> 버튼을 사용하면 대상 파일 시스템을 선택할 수 있으며, 기본값은 <point>ext4</point>입니다. <point>ext4</point> 또는 <point>xfs</point>를 파일 시스템으로 선택하면 설치 프로그램은 LVM을 사용하며, LVM 공간을 제한하는 추가 옵션을 제공합니다.<br>

Proxmox VE는 <point>ZFS</point>에도 설치할 수 있습니다. ZFS는 여러 소프트웨어 RAID 레벨을 제공하므로 하드웨어 RAID 컨트롤러가 없는 시스템을 위한 옵션입니다. 옵션 대화 상자에서 대상 디스크를 선택해야 하며, *Advanced Options*에서 더 많은 ZFS 관련 설정을 변경할 수 있습니다.

> ![](../_static/images/pin.png) 중요<br>
> 하드웨어 RAID 위에 ZFS를 사용하는 것은 지원되지 않으며 데이터 손실을 초래할 수 있습니다.

<br><br>

### 2.3.4.기본 구성 설정
<!-- 사진첨부 -->
다음 페이지에서는 위치, 시간대, 키보드 레이아웃과 같은 기본 구성 옵션을 묻는 메시지가 표시됩니다. 위치는 업데이트 속도를 높이기 위해 가까운 다운로드 서버를 선택하는 데 사용됩니다. 일반적으로 설치 프로그램이 이러한 설정을 자동으로 감지할 수 있으므로 자동 감지에 실패하거나 해당 국가에서 일반적으로 사용하지 않는 키보드 레이아웃을 사용하려는 경우에만 변경하면 됩니다.<br><br>

### 2.3.5.비밀번호 및 이메일 지정

<!-- 사진첨부 -->
다음으로 슈퍼유저(root)의 비밀번호와 이메일 주소를 지정해야 합니다. 비밀번호는 최소 5자 이상으로 구성되어야 합니다. 몇 가지 가이드라인은 다음과 같습니다:<br>
* 최소 12자 이상의 비밀번호를 사용하세요.
* 소문자 및 대문자, 숫자, 기호를 포함하세요.
* 문자 반복, 키보드 패턴, 일반적인 사전 단어, 문자 또는 숫자 시퀀스, 사용자 아이디 그리고 신상 정보(예: ID 등)는 피하세요.<br>

이메일 주소는 시스템 관리자에게 알림을 보내는 데 사용됩니다. 예를 들면 다음과 같습니다:<br>

* 사용 가능한 패키지 업데이트에 대한 정보.
* 주기적인 cron 작업의 오류 메시지.

이러한 모든 내용은 지정된 이메일 주소로 전송됩니다.<br><br>

### 2.3.6.네트워크 구성
<!-- 사진첨부 -->
마지막 단계는 네트워크 구성입니다. 현재 업링크(<point>UP</point>) 상태인 네트워크 인터페이스는 드롭다운 메뉴에서 이름 앞에 채워진 원이 표시됩니다. 설치하는 동안 IPv4 또는 IPv6 주소 중 하나를 지정할 수 있지만 둘 다 지정할 수는 없다는 점에 유의하세요. 듀얼 스택 노드를 구성하려면 설치 후 IP 주소를 추가하세요.<br><br>

### 2.3.7.최종 확인
<!-- 사진첨부 -->
다음 단계에서는 이전에 선택한 옵션들의 요약을 보여줍니다. 모든 설정을 다시 확인하고 변경이 필요한 경우 <point>Previous</point> 버튼을 사용하세요.<br>

<point>Install</point>을 클릭하면 설치 프로그램이 디스크를 포맷하고 패키지를 대상 디스크에 복사하기 시작합니다. 이 단계가 완료될 때까지 기다린 다음, 설치 미디어를 제거하고 시스템을 다시 시작하세요.<br>

패키지 복사는 주로 설치 미디어의 속도와 대상 디스크 성능에 따라 몇 분 정도 소요됩니다. 패키지 복사 및 설정이 완료되면 서버를 재부팅할 수 있습니다. 기본적으로 몇 초 후에 자동으로 재부팅됩니다.<br><br>

## 2.4.설치 후 관리 인터페이스 액세스
시스템을 성공적으로 설치하고 재부팅한 후 Proxmox VE 웹 인터페이스를 사용하여 추가 구성을 할 수 있습니다.<br>

> ![](../_static/images/pin.png) 참고<br>
> 기본적으로 Proxmox VE 웹 인터페이스 접속은 <point>포트 8006</point> 을 사용합니다.

1. 설치 당시 입력한 Proxmox VE IP주소 + 포트 8006을 입력합니다.
    * ex) https://proxmox-ip:8006
2. 설치 시 선택한 <point>root</point>(realm <point>PAM</point>) 사용자 이름과 비밀번호를 사용하여 로그인합니다.(realm PAM) 
3. 엔터프라이즈 리포지토리에 액세스하려면 구독 키를 업로드합니다. 그렇지 않으면 보안 수정, 버그 수정 및 새 기능에 대한 업데이트를 받으려면 테스트가 덜 완료된 공개 패키지 리포지토리 중 하나를 설정해야 합니다.
4. IP 구성과 호스트네임을 확인합니다.
5. 시간대를 확인합니다.
6. 방화벽 설정을 확인합니다.

## 2.5. 파일시스템 구성 고급 옵션

### 2.5.1. 고급 LVM 구성 옵션

설치 프로그램은 <point>pve</point>라는 볼륨 그룹(VG)을 생성하고, <point>ext4</point> 또는 <point>xfs</point>를 사용하는 경우 <point>root</point>, <point>data</point> 및 <point>swap</point>이라는 추가 논리 볼륨(LV)을 생성합니다. 이러한 볼륨의 크기를 제어하려면:<br>
* hdsize
  * 사용할 총 하드 디스크 크기를 정의합니다. 이렇게 하면 추가 파티셔닝을 위해 하드 디스크의 여유 공간을 확보할 수 있습니다
  * 예: 동일한 하드 디스크에 LVM 스토리지에 사용할 수 있는 추가 PV 및 VG
* swapsize
  * <point>swap</point> 볼륨의 크기를 정의합니다. 
  * 기본값은 설치된 메모리의 크기(최소 4GB, 최대 8GB)입니다. 결과 값은 <point>hdsize/8</point>보다 클 수 없습니다.
  > ![](../_static/images/pin.png) 참고<br>
  > 0으로 설정하면 swap 볼륨이 생성되지 않습니다.
* maxroot
  * 운영 체제를 저장하는 <point>root</point> 볼륨의 최대 크기를 정의합니다. root 볼륨 크기의 최대 제한은 <point>hdsize/4</point>입니다.
* maxvz
  * <point>data</point> 볼륨의 최대 크기를 정의합니다. 데이터 볼륨의 실제 크기는 다음과 같습니다:<br>
  `datasize = hdsize - rootsize - swapsize - minfree`<br>
  여기서 <point>datasize</point>는 <point>maxvz</point>보다 클 수 없습니다.
  > ![](../_static/images/pin.png) 참고<br> LVM 씬의 경우, 데이터 풀은 데이터 크기가 4GB보다 큰 경우에만 생성됩니다.<br>
  > 0으로 설정하면 데이터 볼륨이 생성되지 않으며 스토리지 구성이 그에 따라 조정됩니다.
* minfree
  * LVM 볼륨 그룹 pve에 남겨야 하는 여유 공간을 정의합니다. 
  * 128GB 이상의 스토리지를 사용할 수 있는 경우 기본값은 16GB이며, 그렇지 않은 경우 hdsize/8이 사용됩니다.
  > ![](../_static/images/pin.png) 중요<br>
  > LVM은 스냅샷 생성을 위해 VG에 여유 공간이 필요합니다(lvmthin 스냅샷에는 필요하지 않음).

  <br><br>

### 2.5.2. 고급 ZFS 구성 옵션 

ZFS를 사용하는 경우 설치 프로그램이 ZFS 풀, <point>rpool</point>을 생성합니다. 스왑 공간은 생성되지 않지만 설치 디스크의 파티션되지 않은 일부 공간을 스왑을 위해 예약할 수 있습니다. 설치 후 swap zvol을 생성할 수도 있지만 문제가 발생할 수 있습니다.<br>
* ashift
  * 생성된 풀의 <point>ashift</point> 값을 정의합니다. 최소 기본 디스크의 섹터 크기(ashift의 거듭제곱에 2를 곱한 값이 섹터 크기) 또는 풀에 넣을 수 있는 모든 디스크(예: 결함이 있는 디스크 교체)로 설정해야 합니다.
* compress
  * <point>rpool</point>에 압축을 사용할지 여부를 정의합니다.
* pinsum
  * <point>rpool</point>에 사용할 체크섬 알고리즘을 정의합니다.
* copies
  * <point>rpool</point>에 대한 <point>copies</point> 매개변수를 정의합니다. 
* ARC 최대 크기
  * ARC가 커질 수 있는 최대 크기를 정의하여 ZFS가 사용할 메모리 양을 제한합니다.
* hdsize
  * 사용할 총 하드 디스크 크기를 정의합니다. 이는 추가 파티셔닝(예: 스왑 파티션 생성)을 위해 하드 디스크의 여유 공간을 절약하는 데 유용합니다.
  * <point>hdsize</point>는 부팅 가능한 디스크, 즉 RAID0, RAID1 또는 RAID10의 첫 번째 디스크 또는 미러 및 RAID-Z[123]의 모든 디스크에 대해서만 적용됩니다.<br><br>

### 2.5.3. 고급 BTRFS 구성 옵션 

BTRFS를 사용할 때는 스왑 공간이 생성되지 않지만 설치 디스크에 파티션되지 않은 공간을 스왑을 위해 예약할 수 있습니다. 별도의 파티션, BTRFS 서브볼륨 또는 스왑파일을 만들려면 <point>btrfs filesystem mkswapfile</point> 명령을 사용하여 스왑파일을 만들 수 있습니다.
* compress
  * BTRFS 서브볼륨에 대해 압축을 사용할지 여부를 정의합니다. 
  * 다양한 압축 알고리즘이 지원됩니다: <point>on</point>(<point>zlib</point>와 동일), <point>zlib</point>, <point>lzo</point> 및 <point>zstd</point>. 기본값은 <point>off</point>입니다.
* hdsize
  * 사용할 총 하드 디스크 크기를 정의합니다. 이는 추가 파티셔닝(예: 스왑 파티션 만들기)을 위해 하드 디스크의 여유 공간을 절약하는 데 유용합니다.

<br><br>

### 2.5.4. ZFS 성능 팁
ZFS는 많은 메모리에서 가장 잘 작동합니다. ZFS를 사용하려는 경우 충분한 RAM을 사용할 수 있는지 확인하십시오. 각 TB RAW 디스크 공간에 대해 4GB와 1GB RAM을 더하는 것이 좋습니다.<br>
ZFS는 ZIL(ZFS Intent Log)이라고 하는 전용 드라이브를 쓰기 캐시로 사용할 수 있습니다. 이를 위해 빠른 드라이브(SSD)를 사용하세요. 설치 후 다음 명령을 사용하여 추가할 수 있습니다:

```
# zpool add <pool-name> log </dev/path_to_fast_ssd>
```
<br><br>

## 2.6. Debian에 Proxmox VE 설치 

Proxmox VE는 Debian 패키지 세트로 제공되며 표준 Debian 설치 위에 설치할 수 있습니다. 레포지토리를 구성한 후 다음 명령을 실행해야 합니다:

```
# apt-get update
# apt-get install proxmox-ve
```
기존 설치된 Debian 위에 설치하는 것은 쉬워 보이지만 기본 시스템이 올바르게 설치되어 있고 로컬 저장소를 구성하고 사용하는 방법을 알고 있다고 가정합니다. 또한 네트워크를 수동으로 구성해야 합니다.<br>
일반적으로 이것은 사소한 일이 아니며, 특히 LVM 또는 ZFS를 사용하는 경우에는 더욱 그렇습니다.<br><br><br>
<br><br>