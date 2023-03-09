CREATE TABLE IF NOT EXISTS firewallrules(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    direction CHARACTER(7) NOT NULL CHECK(direction='ingress' OR direction='egress') DEFAULT 'ingress',
    allow BOOLEAN NOT NULL DEFAULT FALSE,
    priority INTEGER NOT NULL CHECK(priority>0 AND priority<=65535) DEFAULT 65000, 
    src_ip INTEGER NOT NULL CHECK(src_ip>=0 AND src_ip<=4294967295) DEFAULT 0, -- 0.0.0.0
    src_mask INTEGER NOT NULL CHECK(src_mask>=0 AND src_mask<=4294967295) DEFAULT 4294967295, --255.255.255.255
    dst_ip INTEGER NOT NULL CHECK(dst_ip>=0 AND dst_ip<=4294967295) DEFAULT 0, -- 0.0.0.0
    dst_mask INTEGER NOT NULL CHECK(dst_mask>=0 AND dst_mask<=4294967295) DEFAULT 4294967295, --255.255.255.255
    protocol VARCHAR(64) default NULL,
    port_start INTEGER NOT NULL CHECK(port_start>=0 AND port_start<=65535) DEFAULT 0,
    port_end INTEGER NOT NULL CHECK(port_end>=0 AND port_end<=65535) DEFAULT 65535
);
