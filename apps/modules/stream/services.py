from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_aio
from .exception import ErrorCode

stream_crud = BaseCRUD("stream-videos", engine_aio)

class StreamServices:
    def __init__(self, stream_crud: BaseCRUD):
        self.stream_crud = stream_crud

    async def create(self, data: dict):
        result = await self.stream_crud.create(data)      
        return result

    async def update(self, _id: str, data: dict):
        result = await self.stream_crud.update_by_id(_id, data)
        if not result: 
            raise ErrorCode.InvalidStreamId()
        return result
    
    async def get(self, _id):
        result = await self.stream_crud.get_by_id(_id)
        if not result: 
            raise ErrorCode.InvalidStreamId()
        return result

    async def delete(self, _id):
        result = await self.stream_crud.delete_by_id(_id)
        if not result: 
            raise ErrorCode.InvalidStreamId()
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.stream_crud.search(query, page, limit)
        return result

"""
    async def play_list(self, stream_id: str):
        stream = await self.stream_crud.get_by_id(stream_id)
        if not stream:
            raise ErrorCode.InvalidStreamId()

        master_path = stream.get("path")
        if not master_path:
            raise ErrorCode.InvalidM3U8Path()

        abs_path = Path("/opt/python-projects/apps") / master_path.lstrip("/")
        if not abs_path.exists():
            raise ErrorCode.M3U8FileNotFound()

        resolutions = []
        with open(abs_path, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith("#EXT-X-STREAM-INF"):
                info = line.strip().split(",")
                bandwidth = int(info[0].split("=")[1])
                resolution = info[1].split("=")[1]
                path = lines[i + 1].strip()
                resolutions.append({
                    "bandwidth": bandwidth,
                    "resolution": resolution,
                    "path": path
                })

        result = {"stream_id": str(stream["_id"]), "ratio": stream.get("ratio"), "resolutions": resolutions}
        
        return result
    
    async def play_video(self, stream_id: str, resolution: str = "auto"):
        stream = await self.stream_crud.get_by_id(stream_id)
        if not stream:
            raise ErrorCode.InvalidStreamId()

        master_path = stream.get("path")
        abs_path = Path("/opt/python-projects/apps") / master_path.lstrip("/")
        # abs_path = Path("/opt/python-projects/apps/assets/stream/dance1/master.m3u8")
        if not abs_path.exists():
            raise ErrorCode.M3U8FileNotFound()

        with open(abs_path, "r") as f:
            lines = f.readlines()

        if resolution == "auto":
            return "\n".join(lines)

        # Tìm playlist theo độ phân giải cụ thể
        output_lines = ["#EXTM3U\n", "#EXT-X-VERSION:3\n"]
        for i, line in enumerate(lines):
            if line.startswith("#EXT-X-STREAM-INF") and resolution in line:
                output_lines.append(line)
                output_lines.append(lines[i + 1])
        if len(output_lines) <= 2:
            raise ErrorCode.ResolutionNotFound()

        return "".join(output_lines)

"""