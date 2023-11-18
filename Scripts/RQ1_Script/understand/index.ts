import creator from './creator';
import extractor from './extractor';
import builder from './builder';
import {error} from '@pyanalyzer/logging';
import {CaseContainer} from '@pyanalyzer/doc-parser';
import {UNIMatcher} from '../../../matchers';
import {readFile} from 'node:fs/promises';

export default async (g: string, c: string, cs: CaseContainer, ocwd: string, exepath: string) => {
  try {
    const data = await readFile(`tests/und/${g}/${c}.json`, 'utf-8');
    // console.log(data.replaceAll(/\s+/g, ' '));
    builder(data);
    return UNIMatcher(cs, 'python', 'u');
  } catch {
    if (await creator(g, c)) {
      const data = await extractor(g, c, ocwd);
      if (data) {
        builder(data);
        return UNIMatcher(cs, 'python', 'u');
      } else {
        error(`Failed to extract understand database on ${g}/${c}`);
      }
    } else {
      error(`Failed to create understand database on ${g}/${c}`);
    }
  }
};
