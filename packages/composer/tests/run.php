<?php

declare(strict_types=1);

use FirmaPanel\TradeCountryData\TradeCountryData;

$autoload = dirname(__DIR__, 3) . '/vendor/autoload.php';
if (is_file($autoload)) {
    require $autoload;
} else {
    require dirname(__DIR__) . '/src/TradeCountryData.php';
}

function check(bool $condition, string $message): void
{
    if (!$condition) {
        throw new RuntimeException($message);
    }
}

check(count(TradeCountryData::datasetNames()) === 9, 'Expected nine datasets.');

foreach (TradeCountryData::datasetNames() as $name) {
    $document = TradeCountryData::loadDataset($name);
    check(
        $document['schema_version'] === TradeCountryData::DATASET_VERSION,
        sprintf('Unexpected schema version for %s.', $name),
    );
    check(
        $document['record_count'] === count($document['records']),
        sprintf('Record count mismatch for %s.', $name),
    );
    check(is_file(TradeCountryData::datasetPath($name)), sprintf('Missing %s.', $name));
}

check(count(TradeCountryData::schemaNames()) === 10, 'Expected ten schemas.');

foreach (TradeCountryData::schemaNames() as $name) {
    $schema = TradeCountryData::loadSchema($name);
    check(
        $schema['$schema'] === 'https://json-schema.org/draft/2020-12/schema',
        sprintf('Unexpected JSON Schema dialect for %s.', $name),
    );
    check(is_file(TradeCountryData::schemaPath($name)), sprintf('Missing %s schema.', $name));
}

$composer = json_decode(
    (string) file_get_contents(dirname(__DIR__, 3) . '/composer.json'),
    true,
    512,
    JSON_THROW_ON_ERROR,
);
check(
    $composer['extra']['firmapanel']['dataset-version'] === TradeCountryData::DATASET_VERSION,
    'Composer dataset version does not match the PHP API.',
);
check(
    str_starts_with(TradeCountryData::readCountriesCsv(), 'iso2,iso3,'),
    'Country CSV was not loaded.',
);

try {
    TradeCountryData::loadDataset('missing');
    throw new RuntimeException('Unknown dataset name was accepted.');
} catch (InvalidArgumentException $exception) {
    check(str_contains($exception->getMessage(), 'Unknown dataset name'), 'Wrong error.');
}

try {
    TradeCountryData::loadSchema('missing');
    throw new RuntimeException('Unknown schema name was accepted.');
} catch (InvalidArgumentException $exception) {
    check(str_contains($exception->getMessage(), 'Unknown schema name'), 'Wrong error.');
}

fwrite(STDOUT, "Composer package checks passed.\n");
