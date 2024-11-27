from django.db import models


class Asignacionaula(models.Model):
    idasignacionaula = models.AutoField(db_column='IdAsignacionAula', primary_key=True)  # Field name made lowercase.
    codigoaula = models.ForeignKey('Aula', models.DO_NOTHING, db_column='CodigoAula', blank=True, null=True)  # Field name made lowercase.
    codigogrupo = models.ForeignKey('Grupo', models.DO_NOTHING, db_column='CodigoGrupo', blank=True, null=True)  # Field name made lowercase.
    codigoturno = models.ForeignKey('Turno', models.DO_NOTHING, db_column='CodigoTurno', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AsignacionAula'

    def __str__(self):
        return f"{self.codigoaula} - Grupo {self.codigogrupo} en Turno {self.codigoturno}"



class Asignaciondocente(models.Model):
    idasignaciondocente = models.AutoField(db_column='IdAsignacionDocente', primary_key=True)  # Field name made lowercase.
    ceduladocente = models.ForeignKey('Docente', models.DO_NOTHING, db_column='CedulaDocente', blank=True, null=True)  # Field name made lowercase.
    codigogrupo = models.ForeignKey('Grupo', models.DO_NOTHING, db_column='CodigoGrupo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AsignacionDocente'

    def __str__(self):
        return f"Docente {self.ceduladocente} asignado a {self.codigogrupo} "



class Asignatura(models.Model):
    codigoasignatura = models.AutoField(db_column='CodigoAsignatura', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    idasignatura = models.CharField(db_column='IdAsignatura', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    codigogrupo = models.ForeignKey('Grupo', models.DO_NOTHING, db_column='CodigoGrupo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Asignatura'

    def __str__(self):
        return f"{self.nombre} - {self.idasignatura}"

class Aula(models.Model):
    codigoaula = models.AutoField(db_column='CodigoAula', primary_key=True)  # Field name made lowercase.
    capacidad = models.IntegerField(db_column='Capacidad')  # Field name made lowercase.
    numeroaula = models.IntegerField(db_column='NumeroAula')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Aula'

    def __str__(self):
        return f"Aula {self.numeroaula}"


class Docente(models.Model):
    ceduladocente = models.CharField(db_column='CedulaDocente', primary_key=True, max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    apellido = models.CharField(db_column='Apellido', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    especialidad = models.CharField(db_column='Especialidad', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Docente'

    def __str__(self):
        return f"{self.nombre} - {self.apellido} -  {self.especialidad}"



class Estudiante(models.Model):
    codestudiante = models.CharField(db_column='CodEstudiante', primary_key=True, max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre1 = models.CharField(db_column='Nombre1', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre2 = models.CharField(db_column='Nombre2', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    apellido1 = models.CharField(db_column='Apellido1', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    apellido2 = models.CharField(db_column='Apellido2', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fechanac = models.CharField(db_column='FechaNac', max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    edad = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='Sexo', max_length=10, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cedulaalumno = models.CharField(db_column='CedulaAlumno', max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    direccionalumno = models.CharField(db_column='DireccionAlumno', max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    codigogrupo = models.ForeignKey('Grupo', models.DO_NOTHING, db_column='CodigoGrupo', blank=True, null=True)  # Field name made lowercase.
    codigotutor = models.ForeignKey('Tutor', models.DO_NOTHING, db_column='CodigoTutor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Estudiante'

    def __str__(self):
        return f"{self.nombre1} {self.nombre2} {self.apellido1} {self.apellido2}"


class Grupo(models.Model):
    codigogrupo = models.AutoField(db_column='CodigoGrupo', primary_key=True)  # Field name made lowercase.
    nivelacademico = models.CharField(db_column='NivelAcademico', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Grupo'

    def __str__(self):
        return f"{self.nivelacademico}"

class Horario(models.Model):
    codigohorario = models.AutoField(db_column='CodigoHorario', primary_key=True)  # Field name made lowercase.
    horainicio = models.TimeField(db_column='HoraInicio')  # Field name made lowercase.
    horafin = models.TimeField(db_column='HoraFin')  # Field name made lowercase.
    codigogrupo = models.ForeignKey(Grupo, models.DO_NOTHING, db_column='CodigoGrupo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Horario'
        
        
    def __str__(self):
        return f"{self.horainicio} - {self.horafin}"


class Inscribe(models.Model):
    idinscripcion = models.AutoField(db_column='IdInscripcion', primary_key=True)  # Field name made lowercase.
    codestudiante = models.ForeignKey(Estudiante, models.DO_NOTHING, db_column='CodEstudiante', blank=True, null=True)  # Field name made lowercase.
    codigoasignatura = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='CodigoAsignatura', blank=True, null=True)  # Field name made lowercase.
    fechainscripcion = models.DateField(db_column='FechaInscripcion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Inscribe'

    def __str__(self):
        return f"{self.codestudiante} inscribió {self.codigoasignatura}"


class Registronotas(models.Model):
    idregistro = models.AutoField(db_column='IdRegistro', primary_key=True)  # Field name made lowercase.
    codestudiante = models.ForeignKey(Estudiante, models.DO_NOTHING, db_column='CodEstudiante', blank=True, null=True)  # Field name made lowercase.
    codigoasignatura = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='CodigoAsignatura', blank=True, null=True)  # Field name made lowercase.
    periodoacademico = models.CharField(db_column='PeriodoAcademico', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    parcial1 = models.DecimalField(db_column='Parcial1', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    parcial2 = models.DecimalField(db_column='Parcial2', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    parcial3 = models.DecimalField(db_column='Parcial3', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    parcial4 = models.DecimalField(db_column='Parcial4', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    notafinal = models.DecimalField(db_column='NotaFinal', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RegistroNotas'

    def __str__(self):
        return f"{self.codestudiante} - {self.codigoasignatura} - {self.parcial1}{self.parcial2}{self.parcial3}{self.parcial4}{self.notafinal}"



class Turno(models.Model):
    codigoturno = models.IntegerField(db_column='CodigoTurno', primary_key=True)  # Field name made lowercase.
    horario = models.CharField(db_column='Horario', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Turno'

    def __str__(self):
        return f"{self.horario}"


class Tutor(models.Model):
    codigotutor = models.AutoField(db_column='CodigoTutor', primary_key=True)  # Field name made lowercase.
    nombretutor = models.CharField(db_column='NombreTutor', max_length=50, db_collation='Modern_Spanish_CI_AS',  blank=True, null=True)  # Field name made lowercase.
    cedulatutor = models.CharField(db_column='CedulaTutor', max_length=20, db_collation='Modern_Spanish_CI_AS',  blank=True, null=True)  # Field name made lowercase.
    nombremadre = models.CharField(db_column='NombreMadre', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cedulamadre = models.CharField(db_column='CedulaMadre', max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nombrepadre = models.CharField(db_column='NombrePadre', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cedulapadre = models.CharField(db_column='CedulaPadre', max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tutor'

    def __str__(self):
        return f"{self.nombremadre} - {self.nombrepadre}"