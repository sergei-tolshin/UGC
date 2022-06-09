// Shard 1
sh.addShard(
    "mongors1/mongors1n1:27017",
    "mongors1/mongors1n2:27017",
    "mongors1/mongors1n3:27017",
)

// Shard 2
sh.addShard(
    "mongors2/mongors2n1:27017",
    "mongors2/mongors2n2:27017",
    "mongors2/mongors2n3:27017",
)
