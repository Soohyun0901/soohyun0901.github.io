# Proxmox Cluster File System(pmxcfs)

Proxmox 클러스터 파일 시스템(“pmxcfs”)은 구성 파일을 저장하는 데이터베이스 기반 파일 시스템으로, <point>corosync</point>를 사용하여 모든 클러스터 노드에 실시간으로 복제됩니다. 이를 사용하여 모든 Proxmox VE 관련 구성 파일을 저장합니다.<br>
파일 시스템은 영구 데이터베이스 내의 모든 데이터를 디스크에 저장하지만 데이터의 사본은 RAM에 상주합니다. 이로 인해 최대 크기에 제한이 있으며 현재 128MB입니다. 이 정도면 수천 대의 가상 머신 구성을 저장하기에 충분합니다.<br>
이 시스템은 다음과 같은 이점을 제공합니다:
* 모든 구성을 모든 노드에 실시간으로 원활하게 복제 가능
* 강력한 일관성 검사를 통해 VM ID 중복을 방지
* 노드가 쿼럼을 잃었을 때 읽기 전용으로 전환
* 모든 노드에 대한 코로싱크 클러스터 구성 자동 업데이트
* 분산 잠금 메커니즘 포함

<br><br>

## 6.1. POSIX 호환성
파일 시스템은 FUSE를 기반으로 하므로 동작은 POSIX와 유사합니다. 그러나 일부 기능은 필요하지 않기 때문에 단순히 구현되지 않았습니다:
* 일반 파일과 디렉터리는 생성할 수 있지만 심볼릭 링크는 생성할 수 없습니다.
* 비어 있지 않은 디렉터리의 이름을 변경할 수 없습니다(이렇게 하면 VMID가 고유하다는 것을 더 쉽게 보장할 수 있기 때문입니다).
* 파일 사용 권한을 변경할 수 없습니다(사용 권한은 경로를 기반으로 함).
* <point>O_EXCL</point> 생성은 원자적이지 않습니다(이전 NFS처럼).
* <point>O_TRUNC</point> 생성은 원자적이지 않음(FUSE 제한)
<br><br>

## 6.2. 파일 접근 권한
모든 파일과 디렉터리는 사용자 <point>root</point>가 소유하며 그룹 <point>www-data</point>를 가집니다. root만 쓰기 권한이 있지만 <point>www-data</point> 그룹은 대부분의 파일을 읽을 수 있습니다. 다음 경로 아래의 파일은 root만 액세스할 수 있습니다:<br>
* <point>/etc/pve/priv/</point>
* <point>/etc/pve/nodes/${NAME}/priv/</point>
<br><br>

## 6.3. 기술
클러스터 통신에는 Corosync 클러스터 엔진을, 데이터베이스 파일에는 SQlite를 사용합니다. 파일 시스템은 FUSE를 사용하여 사용자 공간에서 구현됩니다.<br><br>

## 6.4. 파일 시스템 레이아웃 
파일 시스템은 다음 위치에 마운트됩니다:<br>
* <point>/etc/pve</point>
<br><br>

### 6.4.1. 파일
* <point>authkey.pub</point> : 티켓 시스템에서 사용하는 공개 키

* <point>ceph.conf</point> : Ceph 구성 파일(참고: /etc/ceph/ceph.conf는 이에 대한 심볼릭 링크입니다)

* <point>corosync.conf</point> : Corosync 클러스터 구성 파일(Proxmox VE 4.x 이전에는 이 파일을 cluster.conf라고 불렀음)

* <point>datacenter.cfg</point> : Proxmox VE 데이터 센터 전체 구성(키보드 레이아웃, 프록시, ...)

* <point>domains.cfg</point> : Proxmox VE 인증 도메인

* <point>firewall/cluster.fw</point> : 모든 노드에 적용되는 방화벽 구성

* <point>firewall/[NAME].fw</point> : 개별 노드에 대한 방화벽 구성

* <point>firewall/[VMID].fw</point> : VM 및 컨테이너용 방화벽 구성

* <point>ha/crm_commands</point> : 현재 CRM에서 수행 중인 HA 작업을 표시

* <point>ha/manager_status</point> : 클러스터의 HA 서비스에 관한 JSON 형식 정보

* <point>ha/resources.cfg</point> : 고가용성에서 관리하는 리소스 및 현재 상태

* <point>nodes/[NAME]/config</point> : 노드별 구성

* <point>nodes/[NAME]/lxc/[VMID].conf</point> : LXC 컨테이너에 대한 VM 구성 데이터

* <point>nodes/[NAME]/openvz/</point> : 컨테이너 구성 데이터에 사용되는 Proxmox VE 4.0 이전 버전(사용 중단, 곧 제거됨)

* <point>nodes/[NAME]/pve-ssl.key</point> : pve-ssl.pem에 대한 비공개 SSL 키

* <point>nodes/[NAME]/pve-ssl.pem</point> : 웹 서버용 공개 SSL 인증서(클러스터 CA가 서명)

* <point>nodes/[NAME]/pveproxy-ssl.key</point> : pveproxy-ssl.pem에 대한 비공개 SSL 키(선택 사항)

* <point>nodes/[NAME]/pveproxy-ssl.pem</point> : 웹 서버용 공개 SSL 인증서(체인)(선택 사항, pve-ssl.pem에 대한 재정의)

* <point>nodes/[NAME]/qemu-server/[VMID].conf</point> : KVM VM의 VM 구성 데이터

* <point>priv/authkey.key</point> : 티켓 시스템에서 사용하는 개인 키

* <point>priv/authorized_keys</point> : 인증을 위한 클러스터 구성원의 SSH 키

* <point>priv/ceph*</point> : Ceph 인증 키 및 관련 기능

* <point>priv/known_hosts</point> : 확인을 위한 클러스터 구성원의 SSH 키

* <point>priv/lock/*</point> : 클러스터 전체의 안전한 운영을 위해 다양한 서비스에서 사용하는 잠금 파일

* <point>priv/pve-root-ca.key</point> : 클러스터 CA의 개인 키

* <point>priv/shadow.cfg</point> : PVE 영역 사용자를 위한 섀도 비밀번호 파일

* <point>priv/storage/<STORAGE-ID>.pw</point> : 스토리지의 비밀번호를 일반 텍스트로 포함

* <point>priv/tfa.cfg</point> : Base64로 인코딩된 2단계 인증 구성 파일

* <point>priv/token.cfg</point> : 모든 토큰의 API 토큰 비밀 정보

* <point>pve-root-ca.pem</point> : 클러스터 CA의 공개 인증서

* <point>pve-www.key</point> : CSRF 토큰 생성에 사용되는 개인 키

* <point>sdn/*</point> : 소프트웨어 정의 네트워킹(SDN)을 위한 공유 구성 파일

* <point>status.cfg</point> : Proxmox VE 외부 메트릭 서버 구성

* <point>storage.cfg</point> : Proxmox VE 스토리지 구성

* <point>user.cfg</point> : Proxmox VE 액세스 제어 구성(users/groups/…)

* <point>virtual-guest/cpu-models.conf</point> : 사용자 지정 CPU 모델 저장용

* <point>vzdump.cron</point> : 클러스터 전체 vzdump 백업 작업 일정

<br><br>

### 6.4.2. 심볼릭 링크
클러스터 파일 시스템 내의 특정 디렉토리는 노드의 자체 구성 파일을 가리키기 위해 심볼릭 링크를 사용합니다. 따라서 아래 표에서 가리키는 파일은 클러스터의 각 노드에 있는 서로 다른 파일을 참조합니다.
* <point>local</point> : nodes/[LOCAL_HOST_NAME]
* <point>lxc</point> : nodes/[LOCAL_HOST_NAME]/lxc/
* <point>openvz</point> : nodes/[LOCAL_HOST_NAME]/openvz/ (사용되지 않음, 곧 삭제됨)
* <point>qemu-server</point> : nodes/[LOCAL_HOST_NAME]/qemu-server/

<br><br>

### 6.4.3. 디버깅을 위한 특수 상태 파일 (JSON)
* <point>.version</point> : 파일 버전(파일 수정 감지)
* <point>.members</point> : 클러스터 멤버에 대한 정보
* <point>.vmlist</point> : 모든 VM 목록
* <point>.clusterlog</point> : 클러스터 로그(최근 50개 항목)
* <point>.rrd</point> : RRD 데이터(가장 최근 항목)

<br><br>

### 6.4.4. 디버깅 활성화/비활성화 
다음을 사용하여 자세한 syslog 메시지를 활성화할 수 있습니다:
```
echo “1” >/etc/pve/.debug
```
그리고 다음과 같이 상세 정보 표시를 비활성화할 수 있습니다:
```
echo “0” >/etc/pve/.debug
```
<br><br>

## 6.5. 복구
하드웨어 문제와 같이 Proxmox VE 호스트에 심각한 문제가 있는 경우 pmxcfs 데이터베이스 파일 <point>/var/lib/pve-cluster/config.db</point>를 복사하여 새 Proxmox VE 호스트로 옮기는 것이 도움이 될 수 있습니다. 새 호스트에서(아무것도 실행되지 않은 상태에서) <point>pve-cluster</point> 서비스를 중지하고 <point>config.db</point> 파일을 교체해야 합니다(필요한 권한 <point>0600</point>). 그런 다음 손실된 Proxmox VE 호스트에 따라 <point>/etc/hostname</point> 및 <point>/etc/hosts</point>를 조정한 후 재부팅하고 확인합니다(VM/CT 데이터도 잊지 마세요).
<br><br>

### 6.5.1. 클러스터 구성 제거 
권장되는 방법은 클러스터에서 노드를 제거한 후 다시 설치하는 것입니다. 이렇게 하면 모든 비밀 클러스터/ssh 키와 모든 공유 구성 데이터가 삭제됩니다.<br>

경우에 따라 재설치하지 않고 노드를 로컬 모드로 되돌리고 싶을 수도 있는데, 이는 재설치하지 않고 노드 분리하기에서 설명합니다.<br><br>

### 6.5.2. 장애가 발생한 노드에서 게스트 복구/이동하기 
<point>nodes/[NAME]/qemu-server/(VM)</point> 및 <point>nodes/[NAME]/lxc/(컨테이너)</point>의 게스트 구성 파일의 경우, Proxmox VE는 포함된 노드 <point>[NAME]</point>을 해당 게스트의 소유자로 간주합니다. 이 개념은 동시 게스트 구성 변경을 방지하기 위해 값비싼 클러스터 전체 잠금 대신 로컬 잠금을 사용할 수 있게 해줍니다.<br>

결과적으로 게스트의 소유 노드에 정전, 차단, 이벤트 등으로 인해 장애가 발생하면 (모든 디스크가 공유 스토리지에 있는 경우에도) (오프라인) 소유 노드의 로컬 잠금을 얻을 수 없으므로 정기적인 마이그레이션이 불가능합니다(모든 디스크가 공유 스토리지에 있는 경우에도). HA 관리 게스트의 경우, Proxmox VE의 고가용성 스택에는 차단된 노드에서 게스트의 올바른 자동 복구를 보장하는 데 필요한 (클러스터 전체) 잠금 및 감시 기능이 포함되어 있으므로 이는 문제가 되지 않습니다.<br>

HA로 관리되지 않는 게스트에 공유 디스크만 있고 장애가 발생한 노드에서만 사용할 수 있는 다른 로컬 리소스가 없는 경우, 게스트 구성 파일을 <point>/etc/pve/</point>의 장애 노드 디렉토리에서 온라인 노드 디렉토리로 이동(게스트의 논리적 소유자 또는 위치 변경)하는 것만으로 수동 복구가 가능합니다.<br>

예를 들어, 오프라인 <point>노드1</point>에서 다른 노드 <point>노드2</point>로 <point>ID 100</point>의 VM을 복구하려면 클러스터의 모든 구성원 노드에서 root로 다음 명령을 실행하면 됩니다:
```
mv /etc/pve/nodes/node1/qemu-server/100.conf /etc/pve/nodes/node2/qemu-server/
```

>  이와 같이 게스트를 수동으로 복구하기 전에 장애가 발생한 소스 노드의 전원이 실제로 꺼져 있는지/차단되어 있는지 반드시 확인하세요. 그렇지 않으면 mv 명령에 의해 Proxmox VE의 잠금 원칙이 위반되어 예기치 않은 결과가 발생할 수 있습니다.

> 로컬 디스크(또는 오프라인 노드에서만 사용할 수 있는 기타 로컬 리소스)가 있는 게스트는 이와 같이 복구할 수 없습니다. 실패한 노드가 클러스터에 다시 추가될 때까지 기다리거나 백업에서 이러한 게스트를 복원하세요.

<br><br><br>