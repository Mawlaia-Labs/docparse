export {
  FieldType,
  FieldSpec,
  ExtractionSchema,
  ExtractionResult,
  FieldValue,
  PageContent,
  DocumentLayout,
  makeField,
  fieldNames,
  promptLines,
  clampedFieldValue,
  getValue,
  getConfidence,
  missingRequired,
  makeLayout,
  pageCount,
  textForPages,
  allTables,
} from "./models";

export { fromText, load } from "./loader";
export { LLMExtractor, LLMExtractorOptions } from "./extractor";
export {
  INVOICE_SCHEMA,
  LOAN_APPLICATION_SCHEMA,
  W2_SCHEMA,
  NDA_SCHEMA,
  CONTRACT_SCHEMA,
  REGISTRY,
} from "./schemas";

export { AsyncJobClient } from "./async_client";
export type { AsyncJobClientOptions, DocparseJob } from "./async_client";

export const VERSION = "0.3.0";
