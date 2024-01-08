// write a typescript class that represents the structure of the above JSON
// and write a function that takes the above JSON and returns an instance of the class
import type {Reference} from "$lib/references/references";
import {referenceFromJson} from "$lib/references/references";
import type {Link} from "$lib/references/links";
import {linkFromJson} from "$lib/references/links";

export enum TextSegmentType {
  Paragraph = "Paragraph",
  Section = "Section",
  Sentence = "Sentence",
  TextSpan = "TextSpan",
  Enumeration = "Enumeration",
  Litera = "Litera",
  SubLitera = "SubLitera",
  Reference = "Reference",
  Law = "Law",
  Area = "Area",
  Link = "Link",
}

export class TextSegment {
  id?: string;
  type!: TextSegmentType;
  title?: string;
  abbreviation?: string;
  ordinal?: string;
  content?: TextSegment[] | TextSegment | string;
  text?: string;
  url?: string;
  source?: string;
  references?: Reference[];
  links?: TextSegment[];
}

// write a function to convert the above JSON to an instance of the class TextSegment
export function textSegmentFromJson(json: {
  type: string;
  abbreviation?: string;
  source?: string;
  title?: string;
  content?: any;
  text?: string;
  ordinal?: string;
  id?: string;
  url?: string;
  references?: string;
  links?:string;
}): TextSegment {
  const textSegment = new TextSegment();
  textSegment.type = json.type as TextSegmentType;
  textSegment.ordinal = json.ordinal;
  textSegment.abbreviation = json.abbreviation;
  textSegment.title = json.title;
  textSegment.url = json.url;
  textSegment.source = json.source;
  textSegment.text = json.text;

  if(json.links === undefined){
    textSegment.links = [];
  } else if (json.links.constructor === Array) {
    textSegment.links = json.links.map(linkFromJson);
  } else {
    throw new Error("Invalid content type");
  }

  if(json.references === undefined){
    textSegment.references = [];
  } else if (json.references.constructor === Array) {
    textSegment.references = json.references.map(referenceFromJson);
  } else if (typeof json.content === "string") {
    textSegment.content = json.content;
  } else {
    throw new Error("Invalid content type");
  }

  if (json.content === undefined) {
    return textSegment;
  }

  if (json.content.constructor === Array) {
    textSegment.content = json.content.map(textSegmentFromJson);
  } else if (typeof json.content === "object") {
    textSegment.content = textSegmentFromJson(json.content);
  } else if (typeof json.content === "string" ) {
    if(textSegment.type === TextSegmentType.TextSpan || textSegment.type === TextSegmentType.Reference) {
      textSegment.content = json.content;
    } else if (textSegment.type === TextSegmentType.Sentence || textSegment.type === TextSegmentType.Paragraph || textSegment.type === TextSegmentType.Section) {
      let text = json.content;
      textSegment.content = textSegmentFromJson({ "type":"TextSpan", "content":text} );
    } else {
      console.log("Weird content for "+textSegment.type+": "+json.content);
      textSegment.content = json.content;
    }

  } else {
    throw new Error("Invalid content type");
  }
  textSegment.id = json.id;
  return textSegment;
}
