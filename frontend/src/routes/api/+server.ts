import type { RequestEvent } from "./$types";
import fs from "fs";

export function GET({ url } : RequestEvent)
{
    let lawID: string;
    lawID = url.searchParams.get('lawID') ?? 'No ID provided';

    let toRet;
    console.log("Requested law: " + lawID)
    try{
        toRet = fs.readFileSync("./data/"+lawID+".json", "utf8");
    }catch(e){
        console.log(e);
    }


    return new Response(toRet);
}