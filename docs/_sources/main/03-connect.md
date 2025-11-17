# 3. 연결 및 구성

정상적으로 버트온 웹페이지에 접속되었다면 그 다음에 해야하는 설정은 사용 중인 Proxmox 노드를 연결하는 것입니다.<br>
아래 단계를 수행하여 운영 중인 Proxmox 클러스터 및 노드를 연결하세요.<br><br>

## 3.1. 호스트 연결 단계

1. 왼쪽의 <point>설정</point> 탭으로 이동합니다.
2. 연결할 Proxmox 호스트 정보를 입력합니다.
![](../_static/images/main/connect1.png)<br>
    - <point>호스트</point> : Proxmox에 접근하기 위한 IP주소 혹은 도메인을 입력
    - <point>포트</point> : Proxmox API는 HTTPS 프로토콜을 사용하고, 기본값은 8006
    - <point>사용자 이름</point> : 로그인할 계정을 입력(예: root@pam)
    - <point>비밀번호</point> : 위 로그인 계정의 비밀번호를 입력

3. 입력한 정보를 확인한 후, 아래 <point>연결테스트</point> 버튼을 클릭하여 통신 가능 여부를 확인합니다.
> ![](../_static/images/alert.svg) 3번에서 연결이 실패된 경우, 입력 정보와 호스트 현 상태를 확인하세요.


4. 정상적으로 통신 가능한 경우, <point>설정 저장</point>을 눌러 호스트 정보를 저장합니다.<br><br>

## 3.2. 연결 동작 확인
<point>대시보드</point> 탭을 눌러 노드 정보, VM 리스트, 스토리지 정보 등이 정상적으로 표시되는지 확인합니다. 필요한 경우 모니터링 및 알람 설정을 추가로 구성합니다.<br>

> ※ 컨테이너는 <point>--restart unless-stopped</point> 설정으로 되어 있어 VM 재부팅 시 자동으로 재실행됩니다.

> ※ 인증서는 <point>/app/certs</point> 디렉토리에 위치하며, 자체 서명 인증서를 사용합니다.

<br><br><br><br>