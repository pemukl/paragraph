import type { RequestEvent } from "./$types";
import fs from "fs";

export function GET({ url } : RequestEvent)
{
    let lawID: string;
    lawID = url.searchParams.get('lawID') ?? 'No ID provided';

    let toRet;
    try{
        toRet = fs.readFileSync("./data/eWpG.json", "utf8");
    }catch(e){
        console.log(e);
    }
    console.log("Requested law: " + lawID)

    return new Response(toRet);
}