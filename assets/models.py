from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Asset(models.Model):
    '''
    CMDB资产管理系统总表
    '''
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )

    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name='资产类型')
    name = models.CharField(max_length=64, unique=True, verbose_name='资产名称')
    sn = models.CharField(max_length=128, unique=True, verbose_name='资产序列号')
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='所属业务线', on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='设备状态')

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name='制造商', on_delete=models.CASCADE)
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP地址')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='资产管理员', related_name='admin', on_delete=models.CASCADE)
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='所在机房', on_delete=models.CASCADE)
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='合同', on_delete=models.CASCADE)

    purchase_day = models.DateField(null=True, blank=True, verbose_name='购买日期')
    expire_day = models.DateField(null=True, blank=True, verbose_name='过保日期')
    price = models.FloatField(null=True, blank=True, verbose_name='购买价格')

    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='审批人', related_name='approved_by', on_delete=models.CASCADE)
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    a_time = models.DateTimeField(auto_now_add=True, verbose_name='审批时间')
    u_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '<{}> {}'.format(self.get_asset_type_display(), self.name)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'
        ordering = ['-a_time']



class Server(models.Model):
    '''
    服务器设备表
    '''
    sub_asset_type_choice = (
        (0, 'PC服务器'),
        (1, '刀片服务器'),
        (2, '小型机'),
    )

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手动添加'),
    )

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='服务器类型')
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name='添加方式')
    hosted_on = models.ForeignKey('self', null=True, blank=True, verbose_name='宿主机',
                                  related_name='hosted_on_server', on_delete=models.CASCADE)
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=256, null=True, blank=True, verbose_name='RAID类型')
    os_type = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统类型')
    os_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统名称')
    os_release = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统版本')

    def __str__(self):
        return '{}--{}--{} <sn:{}>'.format(self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'



class SecurityDevice(models.Model):
    '''
    安全设备表
    '''
    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (3, '运维审计系统'),
    )

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='安全设备类型')
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='安全设备型号')

    def __str__(self):
        return '{}--{}--{} <sn:{}>'.format(self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = '安全设备'



class StorageDevice(models.Model):
    '''
    存储设备表
    '''
    sub_asset_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁带库'),
        (3, '磁带机'),
    )

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='存储设备类型')
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='存储设备型号')

    def __str__(self):
        return '{}--{}--{} <sn:{}>'.format(self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = '存储设备'



class NetworkDevice(models.Model):
    '''
    网络设备表
    '''
    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡设备'),
        (3, 'VPN设备'),
    )

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='网络设备类型')
    vlan_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='VLAN IP地址')
    intranet_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='内网IP地址')
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='网络设备型号')
    firmware = models.CharField(max_length=128, null=True, blank=True, verbose_name='设备固件版本')
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name='端口个数')
    config_detail = models.TextField(null=True, blank=True, verbose_name='详细配置')

    def __str__(self):
        return '{}--{}--{} <sn:{}>'.format(self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'



class Software(models.Model):
    '''
    付费购买的软件表
    '''
    sub_asset_type_choice = (
        (0, '操作系统'),
        (1, '办公软件'),
        (2, '开发软件'),
        (3, '应用软件'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='软件类型')
    software_version = models.CharField(max_length=128, unique=True, help_text='例如：MS Office 2016 Professional',
                                        verbose_name='软件版本')
    license_key = models.CharField(max_length=128, null=True, blank=True, verbose_name='License Key')
    license_num = models.SmallIntegerField(default=1, verbose_name='License 数量')

    def __str__(self):
        return '{}--{}'.format(self.software_version, self.get_sub_asset_type_display())

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = '软件/系统'



class Manufacturer(models.Model):
    '''
    制造商表
    '''
    name = models.CharField(max_length=64, unique=True, verbose_name='制造商名称')
    telephone = models.CharField(max_length=30, null=True, blank=True, verbose_name='支持电话号码')
    memo = models.CharField(max_length=128, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '制造商'
        verbose_name_plural = '制造商'



class IDC(models.Model):
    '''
    机房表
    '''
    name = models.CharField(max_length=64, unique=True, verbose_name='机房名称')
    memo = models.CharField(max_length=128, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = '机房'



class BusinessUnit(models.Model):
    '''
    业务线表
    '''
    parent_unit = models.ForeignKey('self', null=True, blank=True, related_name='parent_level', on_delete=models.SET_NULL)
    name = models.CharField(max_length=64, unique=True, verbose_name='业务线名称')
    memo = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = '业务线'



class Contract(models.Model):
    '''
    合同表
    '''
    sn = models.CharField(max_length=64, unique=True, verbose_name='合同编号')
    name = models.CharField(max_length=128, verbose_name='合同名称')
    memo = models.TextField('备注', null=True, blank=True)
    price = models.IntegerField('合同金额')
    description = models.TextField('合同描述', null=True, blank=True)
    start_day = models.DateField('合同开始日期', null=True, blank=True)
    end_day = models.DateField('合同结束日期', null=True, blank=True)
    c_datetime = models.DateTimeField('创建时间', auto_now_add=True)
    u_datetime = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = '合同'



class Tag(models.Model):
    '''
    标签
    '''
    name = models.CharField('标签名称', max_length=32, unique=True)
    c_datetime = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'



class CPU(models.Model):
    '''
    CPU组件
    '''
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    cpu_model = models.CharField('CPU型号', max_length=128,null=True, blank=True)
    cpu_count = models.PositiveSmallIntegerField('CPU个数', default=1)
    cpu_core_count = models.PositiveSmallIntegerField('CPU内核数', default=1)

    def __str__(self):
        return '{}:{}'.format(self.asset.name, self.cpu_model)

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPU'



class RAM(models.Model):
    '''
    内存组件
    '''
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    sn = models.CharField('序列号', max_length=128, null=True, blank=True)
    model = models.CharField('内存型号', max_length=128, null=True, blank=True)
    brand = models.CharField('内存品牌', max_length=128, null=True, blank=True)
    slot_num = models.CharField('插槽号', max_length=64)
    size = models.CharField('内存大小(G)', null=True, blank=True)

    def __str__(self):
        return '{}:{} 内存大小(G):{}'.format(self.asset.name, self.model, self.size)

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = '内存'
        # 联合约束，同一资产下asset和slot_num不能相同，必须联合唯一
        unique_together = ('asset', 'slot_num')



class Disk(models.Model):
    '''
    硬盘组件
    '''
    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    sn = models.CharField('序列号', max_length=128, null=True, blank=True)
    slot_num = models.CharField('插槽号', max_length=64, null=True, blank=True)
    model = models.CharField('硬盘型号', max_length=128, null=True, blank=True)
    brand = models.CharField('硬盘品牌', max_length=128, null=True, blank=True)
    size = models.CharField('硬盘大小(G)', null=True, blank=True)
    disk_interface_type = models.CharField('接口类型',max_length=16, choices=disk_interface_type_choice, default='unknown')

    def __str__(self):
        return '{}:{} 硬盘大小(G):{}'.format(self.asset.name, self.model, self.size)

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = '硬盘'
        # 联合约束，同一资产下asset和slot_num不能相同，必须联合唯一
        unique_together = ('asset', 'slot_num')



class NIC(models.Model):
    '''
    网卡组件
    '''
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    name = models.CharField('网卡名称', max_length=64, blank=True, null=True)
    model = models.CharField('网卡型号', max_length=128)
    mac = models.CharField('网卡MAC地址', max_length=64)  # 虚拟机有可能会出现同样的mac地址
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
    subnet_mask = models.CharField('子网掩码', max_length=64, blank=True, null=True)
    bonding = models.CharField('绑定地址', max_length=64, blank=True, null=True)

    def __str__(self):
        return '{}:{} MAC:{}'.format(self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = "网卡"
        unique_together = ('asset', 'model', 'mac')



class EventLog(models.Model):
    '''
    资产日志表
    在关联对象被删除的时候，不能一并删除，需保留日志。
    因此，on_delete=models.SET_NULL
    '''
    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '变更'),
    )

    asset = models.ForeignKey(Asset, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField('事件日志名称', max_length=128)
    new_asset = models.ForeignKey('NewApprovalZone', null=True, blank=True, on_delete=models.SET_NULL)
    event_type = models.CharField('事件日志类型', choices=event_type_choice, default=4)
    component = models.CharField('事件子项',max_length=256, null=True, blank=True)
    detail = models.TextField('事件内容')
    c_datetime = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True,verbose_name='事件所属人', on_delete=models.SET_NULL)
    memo = models.TextField('事件备注', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '事件日志'
        verbose_name_plural = '事件日志'



class NewApprovalZone(models.Model):
    '''
    新资产审批区
    '''
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )

    asset_type = models.CharField('资产类型',max_length=64, choices=asset_type_choice, default='server', null=True, blank=True)
    sn = models.CharField('序列号', max_length=128, unique=True)
    manufacturer = models.CharField('制造商', max_length=64, null=True, blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    ram_size = models.PositiveSmallIntegerField('内存大小(G)', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)
    cpu_count = models.PositiveSmallIntegerField('CPU个数', default=1)
    cpu_core_count = models.PositiveSmallIntegerField('CPU内核数', default=1)
    os_type = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统类型')
    os_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统名称')
    os_release = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统版本')
    data = models.TextField('资产数据')
    c_datetime = models.DateTimeField('创建时间', auto_now_add=True)
    u_datetime = models.DateTimeField('更新时间', auto_now=True)
    approve_flag = models.BooleanField('是否批准', default=False)

    def __str__(self):
        return f'{self.sn}'

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = '新上线待批准资产'
        ordering = ['-c_datetime']