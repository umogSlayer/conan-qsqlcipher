// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
#include "qsql_sqlite_p.h"
#include <qsqlcipher_export.h>

#include <QSqlDriverPlugin>
#include <QStringList>

using namespace Qt::StringLiterals;

class QSQLCIPHER_EXPORT QSQLCipherDriverPlugin : public QSqlDriverPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QSqlDriverFactoryInterface" FILE "sqlcipher.json")

public:
    QSQLCipherDriverPlugin();

    QSqlDriver* create(const QString &) override;
};

QSQLCipherDriverPlugin::QSQLCipherDriverPlugin()
    : QSqlDriverPlugin()
{
}

QSqlDriver* QSQLCipherDriverPlugin::create(const QString &name)
{
    if (name == "QSQLCIPHER"_L1) {
        QSQLCipherDriver* driver = new QSQLCipherDriver();
        return driver;
    }

    return nullptr;
}

#include "smain.moc"
