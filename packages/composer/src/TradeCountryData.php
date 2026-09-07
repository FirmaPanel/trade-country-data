<?php

declare(strict_types=1);

namespace FirmaPanel\TradeCountryData;

use InvalidArgumentException;
use JsonException;
use RuntimeException;
use UnexpectedValueException;

final class TradeCountryData
{
    public const DATASET_VERSION = '0.3.0';

    /** @var array<string, string> */
    private const DATASETS = [
        'countries' => 'countries.json',
        'customs-authorities' => 'customs-authorities.json',
        'customs-relationships' => 'customs-relationships.json',
        'official-trade-portals' => 'official-trade-portals.json',
        'regions' => 'regions.json',
        'sources' => 'sources.json',
        'standards-bodies' => 'standards-bodies.json',
        'trade-agencies' => 'trade-agencies.json',
        'trade-groups' => 'trade-groups.json',
    ];

    /** @var array<string, string> */
    private const SCHEMAS = [
        'common' => 'common.schema.json',
        'country' => 'country.schema.json',
        'customs-authority' => 'customs-authority.schema.json',
        'customs-relationship' => 'customs-relationship.schema.json',
        'region' => 'region.schema.json',
        'source' => 'source.schema.json',
        'standards-body' => 'standards-body.schema.json',
        'trade-agency' => 'trade-agency.schema.json',
        'trade-group' => 'trade-group.schema.json',
        'trade-portal' => 'trade-portal.schema.json',
    ];

    private function __construct()
    {
    }

    /** @return list<string> */
    public static function datasetNames(): array
    {
        return array_keys(self::DATASETS);
    }

    /** @return list<string> */
    public static function schemaNames(): array
    {
        return array_keys(self::SCHEMAS);
    }

    /** @return array<string, mixed> */
    public static function loadDataset(string $name): array
    {
        return self::loadJson(self::datasetPath($name));
    }

    /** @return array<string, mixed> */
    public static function loadSchema(string $name): array
    {
        return self::loadJson(self::schemaPath($name));
    }

    public static function datasetPath(string $name): string
    {
        $filename = self::resolveName('dataset', $name, self::DATASETS);

        return self::rootPath() . '/data/' . $filename;
    }

    public static function schemaPath(string $name): string
    {
        $filename = self::resolveName('schema', $name, self::SCHEMAS);

        return self::rootPath() . '/schema/' . $filename;
    }

    public static function readCountriesCsv(): string
    {
        return self::readFile(self::rootPath() . '/data/countries.csv');
    }

    private static function rootPath(): string
    {
        return dirname(__DIR__, 3);
    }

    /**
     * @param array<string, string> $choices
     */
    private static function resolveName(string $kind, string $name, array $choices): string
    {
        if (!array_key_exists($name, $choices)) {
            throw new InvalidArgumentException(sprintf(
                'Unknown %s name %s; choose one of: %s',
                $kind,
                var_export($name, true),
                implode(', ', array_keys($choices)),
            ));
        }

        return $choices[$name];
    }

    private static function readFile(string $path): string
    {
        $contents = @file_get_contents($path);
        if ($contents === false) {
            throw new RuntimeException(sprintf('Unable to read package resource: %s', $path));
        }

        return $contents;
    }

    /** @return array<string, mixed> */
    private static function loadJson(string $path): array
    {
        try {
            $document = json_decode(
                self::readFile($path),
                true,
                512,
                JSON_THROW_ON_ERROR,
            );
        } catch (JsonException $exception) {
            throw new UnexpectedValueException(
                sprintf('Invalid JSON package resource: %s', $path),
                0,
                $exception,
            );
        }

        if (!is_array($document)) {
            throw new UnexpectedValueException(sprintf(
                'JSON package resource is not an object: %s',
                $path,
            ));
        }

        return $document;
    }
}
